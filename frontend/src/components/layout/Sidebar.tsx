import {
  Home,
  Settings,
  Layers,
  ChevronRight,
  ChevronLeft,
} from "lucide-react";
import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

{
  /* To be replaced! */
}
const user = {
  name: "John",
  lastName: "Doe",
  imageUrl: "/images/man.png",
  role: "Admin",
};
{
  /* End of to be replaced! */
}

const navItems = [
  { label: "Home", href: "/dashboard", icon: Home },
  { label: "Datasets", href: "/dashboard/datasets", icon: Layers },
  { label: "Jobs", href: "/dashboard/jobs", icon: Settings },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const toggle = () => setCollapsed((v) => !v);

  const location = useLocation();
  const pathname = location.pathname;

  return (
    <aside
      className={`flex flex-col shrink-0 border-r bg-white/50 p-2 transition-[width] duration-200 ${
        collapsed ? "w-16" : "w-60"
      }`}
    >
      <div
        className={`flex items-center ${
          collapsed ? "justify-center" : "justify-end"
        }`}
      >
        <button
          onClick={toggle}
          aria-pressed={collapsed}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="inline-flex h-8 w-8 items-center justify-center rounded-md hover:bg-gray-100 hover:scale-105 active:scale-95"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </button>
      </div>
      {/* Nav */}
      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            item.href === "/dashboard"
              ? pathname === "/dashboard"
              : pathname === item.href || pathname.startsWith(item.href + "/");

          return (
            <Link key={item.href} to={item.href}>
              <div
                className={`my-1 h-10 rounded-md px-2 hover:bg-gray-100 hover:scale-105 active:scale-95 ${
                  collapsed
                    ? "flex justify-center items-center"
                    : "flex items-center"
                } ${isActive ? "bg-gray-200 font-semibold" : ""}`}
              >
                <Icon className="h-4 w-4 flex-none" />
                {!collapsed && (
                  <span className="ml-2 truncate">{item.label}</span>
                )}
              </div>
            </Link>
          );
        })}
      </nav>
      <footer className="flex mt-auto border-t pt-3">
        <img
          src={user?.imageUrl || "/images/user.png"}
          alt={user?.name || "Unknown User"}
          className="h-10 w-10 rounded-full object-cover justify-items-start"
        />
        {!collapsed && (
          <article className="ml-2">
            <h2 className="truncate text-sm font-medium">
              {user?.name} {user?.lastName}
            </h2>
            <p className="text-xs text-muted-foreground">{user?.role}</p>
          </article>
        )}
      </footer>
    </aside>
  );
}
