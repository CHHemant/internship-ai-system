import Link from "next/link";

const links = [
  ["/", "Landing"],
  ["/dashboard", "Dashboard"],
  ["/upload", "Resume Upload"],
  ["/results", "Results"],
  ["/history", "History"],
  ["/settings", "Settings"],
];

export function Nav() {
  return (
    <nav className="mb-8 flex flex-wrap gap-2 rounded-2xl border border-white/20 bg-black/20 p-3 backdrop-blur">
      {links.map(([href, label]) => (
        <Link
          key={href}
          href={href}
          className="rounded-lg px-3 py-2 text-sm text-white/90 transition hover:bg-white/20"
        >
          {label}
        </Link>
      ))}
    </nav>
  );
}
