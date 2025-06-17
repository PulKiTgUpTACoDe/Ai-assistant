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
    <div className="h-full flex flex-col md:mt-20 mt-4 gap-y-5">
      <div className="px-2 md:p-4">
        <Button
          onClick={handleCreateSession}
          className="w-full text-sm md:text-base h-9 md:h-10"
          disabled={isLoading || isCreating}
        >
          {isCreating ? (
            <Loader2 className="w-3.5 h-3.5 md:w-4 md:h-4 mr-1.5 md:mr-2 animate-spin" />
          ) : (
            <Plus className="w-3.5 h-3.5 md:w-4 md:h-4 mr-1.5 md:mr-2" />
          )}
          New Chat
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto px-1.5 md:p-2">
        <AnimatePresence>
          {sessions.map((session) => (
            <motion.div
              key={session.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="mb-1 md:mb-2"
            >
              <div
                className={`p-1.5 md:p-2 rounded-lg flex items-center justify-between group cursor-pointer ${
                  currentSession?.id === session.id
                    ? "bg-primary/10"
                    : "hover:bg-muted active:bg-muted/80"
                }`}
              >
                {editingSessionId === session.id ? (
                  <div className="flex items-center gap-1 md:gap-2 flex-1">
                    <Input
                      value={newTitle}
                      onChange={(e) => setNewTitle(e.target.value)}
                      className="h-7 md:h-8 text-sm md:text-base px-2 md:px-3"
                      autoFocus
                      disabled={isRenaming}
                    />
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={handleRenameSave}
                      className="h-7 w-7 md:h-8 md:w-8"
                      disabled={isRenaming}
                    >
                      {isRenaming ? (
                        <Loader2 className="h-3 w-3 md:h-4 md:w-4 animate-spin" />
                      ) : (
                        <Check className="h-3 w-3 md:h-4 md:w-4" />
                      )}
                    </Button>
                    <Button
                      size="icon"
                      variant="ghost"
                      onClick={handleRenameCancel}
                      className="h-7 w-7 md:h-8 md:w-8"
                      disabled={isRenaming}
                    >
                      <X className="h-3 w-3 md:h-4 md:w-4" />
                    </Button>
                  </div>
                ) : (
                  <>
                    <div
                      className="flex-1 truncate text-sm md:text-base px-1 md:px-2"
                      onClick={() => selectSession(session.id)}
                    >
                      {session.title}
                    </div>
                    <div className="flex items-center gap-0.5 md:gap-1 opacity-0 group-hover:opacity-100">
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleRenameStart(session)}
                        className="h-7 w-7 md:h-8 md:w-8"
                        disabled={isDeleting === session.id}
                      >
                        <Edit2 className="h-3 w-3 md:h-4 md:w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(session.id)}
                        className="h-7 w-7 md:h-8 md:w-8"
                        disabled={isDeleting === session.id}
                      >
                        {isDeleting === session.id ? (
                          <Loader2 className="h-3 w-3 md:h-4 md:w-4 animate-spin" />
                        ) : (
                          <Trash2 className="h-3 w-3 md:h-4 md:w-4" />
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
