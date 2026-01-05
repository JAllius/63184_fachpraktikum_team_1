import { Fox } from "@/components/watermark/Fox";

type Props = {
  name?: string;
  bypass?: string;
};

const NotFound = ({ name, bypass }: Props) => {
  return (
    <div className="relative min-h-screen bg-background">
      <div className="flex items-center">
        <Fox
          aria-hidden
          size="80%"
          className="pointer-events-none absolute inset-0 z-0 opacity-[0.12] m-auto"
          style={{ color: "hsl(var(--sidebar-foreground))" }}
          nodeFill="hsl(var(--sidebar-foreground))"
        />
      </div>
      <div className="w-full min-h-screen flex items-center justify-center">
        {bypass ? (
          <p className="text-xl font-semibold">{bypass}</p>
        ) : (
          <p className="text-xl font-semibold">
            {name ?? "File"} was not found.
          </p>
        )}
      </div>
    </div>
  );
};

export default NotFound;
