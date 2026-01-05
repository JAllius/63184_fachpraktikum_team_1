import { Fox } from "@/components/watermark/Fox";
import { TypewriterText } from "../app/Typewriter";
import { useCallback, useState } from "react";

const Loading = () => {
  const [reverse, setReverse] = useState(false);
  const handleReverse = useCallback(() => {
    setReverse((v) => !v);
  }, []);

  return (
    <div className="relative min-h-screen bg-background p-8 flex items-center justify-center">
      <div className="flex items-center">
        <Fox
          aria-hidden
          size="80%"
          className="pointer-events-none absolute inset-0 z-0 opacity-[0.12] m-auto"
          style={{ color: "hsl(var(--sidebar-foreground))" }}
          nodeFill="hsl(var(--sidebar-foreground))"
        />
      </div>
      <div className="relative z-10 h-full flex items-center justify-center flex-col select-none">
        <div className="font-mono text-4xl md:text-6xl text-muted-foreground tracking-tight">
          <TypewriterText
            text="< Loading... />"
            reverse={reverse}
            onDone={() => setTimeout(handleReverse, 3000)}
            keepCursor={true}
          />
        </div>
      </div>
    </div>
  );
};

export default Loading;
