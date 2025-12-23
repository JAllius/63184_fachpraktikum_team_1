import { TypewriterText } from "@/components/app/Typewriter";
import { FoxWatermark } from "@/components/io/test";
import { useCallback, useState } from "react";

export default function AppPage() {
  const [step, setStep] = useState<1 | 2>(1);
  return (
    <div className="min-h-screen flex bg-background">
      <div className="relative w-3/4 border-r p-8 overflow-hidden">
        <FoxWatermark
          aria-hidden
          size="80%"
          className="pointer-events-none absolute inset-0 m-auto opacity-[0.12]"
          style={{ color: "hsl(var(--sidebar-foreground))" }}
          nodeFill="hsl(var(--sidebar-foreground))"
        />
        <div className="relative z-10 h-full flex items-center justify-center flex-col select-none">
          <div className="font-mono text-4xl md:text-6xl text-muted-foreground tracking-tight">
            <TypewriterText
              text="< Predictive_Analytics />"
              onDone={useCallback(() => setStep(2), [])}
            />
          </div>
          {step >= 2 && (
            <div className="font-mono text-xl md:text-2xl text-muted-foreground tracking-tight pt-6">
              <TypewriterText text="// turning data into desicions" />
            </div>
          )}
        </div>
      </div>

      <div className="w-1/4 p-8 flex flex-col gap-4 bg-[hsl(var(--sidebar-background))]">
        <h1 className="text-xl font-semibold">App page</h1>

        <div className="text-sm text-muted-foreground">
          Placeholder for authentication:
        </div>

        <a
          href="/dashboard"
          className="inline-block w-fit rounded-md border px-4 py-2 hover:bg-accent"
        >
          Move to dashboard
        </a>
      </div>
    </div>
  );
}
