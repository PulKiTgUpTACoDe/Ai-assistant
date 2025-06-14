"use client";

import { useState } from "react";
import { useSession } from "@/lib/context/session-context";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Trash2, Edit2, Check, X, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { format } from "date-fns";

export function SessionSidebar() {
  const {
    sessions,
    currentSession,
    isLoading,
    createSession,
    selectSession,
    renameSession,
    deleteSession,
  } = useSession();

  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [isRenaming, setIsRenaming] = useState(false);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);

  const handleCreateSession = async () => {
    try {
      setIsCreating(true);
      await createSession("New Chat");
    } finally {
      setIsCreating(false);
    }
  };

  const handleRenameStart = (session: any) => {
    setEditingSessionId(session.id);
    setNewTitle(session.title);
  };

  const handleRenameSave = async () => {
    if (editingSessionId && newTitle.trim()) {
      try {
        setIsRenaming(true);
        await renameSession(editingSessionId, newTitle.trim());
        setEditingSessionId(null);
      } finally {
        setIsRenaming(false);
      }
    }
  };

  const handleRenameCancel = () => {
    setEditingSessionId(null);
  };

  const handleDelete = async (sessionId: string) => {
    try {
      setIsDeleting(sessionId);
      await deleteSession(sessionId);
    } finally {
      setIsDeleting(null);
    }
  };

  return (
    <div className="h-full flex flex-col md:mt-20 mt-5">
      <div className="p-4">
        <Button
          onClick={handleCreateSession}
          className="w-full"
          disabled={isLoading || isCreating}
        >
          {isCreating ? (
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          ) : (
            <Plus className="w-4 h-4 mr-2" />
          )}
          New Chat
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        <AnimatePresence>
          {sessions.map((session) => (
            <motion.div
              key={session.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-2"
            >
              <div
                className={`p-2 rounded-lg flex items-center justify-between group cursor-pointer ${
                  currentSession?.id === session.id
                    ? "bg-primary/10"
                    : "hover:bg-muted"
                }`}
              >
                {editingSessionId === session.id ? (
                  <div className="flex items-center gap-2 flex-1">
                    <Input
                      value={newTitle}
                      onChange={(e) => setNewTitle(e.target.value)}
                      className="h-8"
                      autoFocus
                      disabled={isRenaming}
                    />
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={handleRenameSave}
                      className="h-8 w-8"
                      disabled={isRenaming}
                    >
                      {isRenaming ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Check className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={handleRenameCancel}
                      className="h-8 w-8"
                      disabled={isRenaming}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ) : (
                  <>
                    <div
                      className="flex-1 truncate"
                      onClick={() => selectSession(session.id)}
                    >
                      {session.title}
                    </div>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100">
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleRenameStart(session)}
                        className="h-8 w-8"
                        disabled={isDeleting === session.id}
                      >
                        <Edit2 className="h-4 w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(session.id)}
                        className="h-8 w-8"
                        disabled={isDeleting === session.id}
                      >
                        {isDeleting === session.id ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Trash2 className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
