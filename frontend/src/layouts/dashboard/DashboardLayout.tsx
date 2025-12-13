import { Outlet } from "react-router-dom";
import Sidebar from "../../components/layout/Sidebar";
import { Toaster } from "sonner";

export default function DashboardLayout() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1">
        <Outlet />
        <Toaster position="bottom-left" />
      </main>
    </div>
  );
}
