import React, { useEffect, useRef, useState } from "react";
import "./app.css";

type Role = "user" | "bot";
type Message = { role: Role; text: string; ts: number };

const SUGGESTIONS = [
  "bonjour",
  "quelle heure",
  "on est quel jour",
  "météo Rabat",
  "je m'appelle Mehdi",
  "qui a créé Python ?",
  "ballon d'or 2023",
  "capital maroc",
  "langue officielle maroc",
  "monnaie maroc",
];

function useLocalStorage<T>(key: string, initial: T) {
  const [v, setV] = useState<T>(() => {
    try {
      const raw = localStorage.getItem(key);
      return raw ? (JSON.parse(raw) as T) : initial;
    } catch {
      return initial;
    }
  });
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(v));
    } catch {}
  }, [key, v]);
  return [v, setV] as const;
}

export default function ChatbotUI() {
  // Thème (light/dark) persistant
  const [theme, setTheme] = useLocalStorage<"light" | "dark">("theme", "light");
  useEffect(() => {
    const body = document.body;
    if (theme === "dark") body.classList.add("dark");
    else body.classList.remove("dark");
  }, [theme]);

  // API base (même origine par défaut : “/”)
  const [apiBase, setApiBase] = useLocalStorage<string>("apiBase", "/");

  // Messages
  const [messages, setMessages] = useLocalStorage<Message[]>("chatHistory", [
    {
      role: "bot",
      text: "Bienvenue 👋 Pose une question ou utilise une suggestion.",
      ts: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const canSend = input.trim().length > 0 && !loading;

  async function send(text: string) {
    const msg = text.trim();
    if (!msg) return;

    setError(null);
    setMessages((m) => [...m, { role: "user", text: msg, ts: Date.now() }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${apiBase.replace(/\/$/, "")}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      const reply =
        (data && (data.reply ?? data.message)) || "(réponse vide)";
      setMessages((m) => [
        ...m,
        { role: "bot", text: String(reply), ts: Date.now() },
      ]);
    } catch {
      setError(
        "Impossible de contacter l'API. Vérifie l'URL et que le serveur tourne."
      );
      setMessages((m) => [
        ...m,
        { role: "bot", text: "(Erreur) API non joignable.", ts: Date.now() },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (canSend) send(input);
    }
  }

  function clearChat() {
    setMessages([
      { role: "bot", text: "Conversation effacée 🧹", ts: Date.now() },
    ]);
  }

  function clickSuggestion(s: string) {
    setInput(s);
  }

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).catch(() => {});
  }

  // -------- Export conversation --------
  function download(filename: string, content: string, mime = "text/plain") {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function exportTxt() {
    const lines = messages.map(
      (m) =>
        `[${new Date(m.ts).toLocaleString()}] ${m.role.toUpperCase()}: ${m.text}`
    );
    download("conversation.txt", lines.join("\n"));
  }

  function exportJson() {
    download("conversation.json", JSON.stringify(messages, null, 2), "application/json");
  }

  return (
    <div className="app-container">
      <div className="chat-card">
        {/* Header */}
        <div className="chat-header">🤖 Mehdi Chatbot</div>

        {/* Toolbar */}
        <div style={{ display: "flex", gap: 8, marginBottom: 12, flexWrap: "wrap" }}>
          <input
            style={{ flex: 1, minWidth: 240 }}
            placeholder="URL API (ex: / ou http://127.0.0.1:8000)"
            value={apiBase}
            onChange={(e) => setApiBase(e.target.value)}
          />
          <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
            {theme === "dark" ? "☀️ Clair" : "🌙 Sombre"}
          </button>
          <button onClick={clearChat}>Effacer</button>
          <button onClick={exportTxt} title="Exporter en .txt">Exporter .txt</button>
          <button onClick={exportJson} title="Exporter en .json">Exporter .json</button>
        </div>

        {/* Messages */}
        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i}>
              <div className={m.role === "user" ? "msg-user" : "msg-bot"}>
                <span style={{ whiteSpace: "pre-wrap" }}>{m.text}</span>
                {/* copier discret */}
                <span
                  title="Copier"
                  onClick={() => copyToClipboard(m.text)}
                  style={{ marginLeft: 8, opacity: 0.6, cursor: "pointer", userSelect: "none" }}
                >
                  📋
                </span>
              </div>
              <div className="msg-time">
                {new Date(m.ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </div>
            </div>
          ))}
          {loading && <div className="msg-bot">Le bot écrit… • • •</div>}
          {error && (
            <div
              style={{
                background: theme === "dark" ? "#451a1a" : "#fee2e2",
                color: theme === "dark" ? "#fecaca" : "#991b1b",
                border: "1px solid #fecaca",
                borderRadius: 8,
                padding: "8px 12px",
                marginTop: 8,
              }}
            >
              {error}
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Suggestions */}
        <div className="suggestions">
          {SUGGESTIONS.map((s) => (
            <button key={s} onClick={() => clickSuggestion(s)}>
              {s}
            </button>
          ))}
        </div>

        {/* Input */}
        <div className="chat-input" style={{ marginTop: 10 }}>
          <textarea
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Écris un message… (Entrée = envoyer, Shift+Entrée = retour)"
            style={{
              flex: 1,
              padding: 10,
              border: "1px solid #cbd5e1",
              borderRadius: 8,
              resize: "none",
              background: "inherit",
              color: "inherit",
            }}
          />
          <button onClick={() => send(input)} disabled={!canSend}>
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}
