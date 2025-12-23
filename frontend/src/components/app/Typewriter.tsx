import { useEffect, useState } from "react";

type Props = {
  text: string;
  speed?: number;
  onDone?: () => void;
};

export function TypewriterText({ text, speed = 80, onDone }: Props) {
  const [value, setValue] = useState("");

  useEffect(() => {
    let i = 0;
    const id = setInterval(() => {
      setValue(text.slice(0, i + 1));
      i++;
      if (i >= text.length) {
        clearInterval(id);
        onDone?.();
      }
    }, speed);

    return () => clearInterval(id);
  }, [text, speed, onDone]);

  return (
    <span className="whitespace-pre">
      {value}
      {value.length !== text.length && (
        <span className="ml-0.5 animate-pulse">▍</span>
      )}
    </span>
  );
}
