import { useTheme } from "./theme.constants";
import { ThemeSwitch } from "../ui/theme-switch";

const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <ThemeSwitch
      checked={isDark}
      onCheckedChange={(checked) => setTheme(checked ? "light" : "dark")}
    />
  );
};

export default ThemeToggle;
