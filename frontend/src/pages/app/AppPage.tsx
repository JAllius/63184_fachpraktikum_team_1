export default function AppPage() {
  return (
    <div className="min-h-auto flex flex-col items-center justify-center">
      <h1>App page</h1>
      <div className="p-2">Placeholder for authentication:</div>
      <div>
        <a href="/dashboard" className="border rounded-md p-2">
          Move to dashboard
        </a>
      </div>
    </div>
  );
}
