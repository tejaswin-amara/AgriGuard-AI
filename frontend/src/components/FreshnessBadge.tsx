import type React from "react";

interface Props {
  state?: string;
}

export const FreshnessBadge: React.FC<Props> = ({ state = "fresh" }) => {
  const getStyle = () => {
    switch (state.toLowerCase()) {
      case "fresh":
        return "bg-emerald-100 text-emerald-800 border-emerald-300";
      case "cached":
        return "bg-sky-100 text-sky-800 border-sky-300";
      case "stale":
        return "bg-amber-100 text-amber-800 border-amber-300";
      default:
        return "bg-rose-100 text-rose-800 border-rose-300";
    }
  };

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${getStyle()}`}
    >
      <span className="w-1.5 h-1.5 mr-1.5 rounded-full bg-current opacity-75" />
      {state.toUpperCase()}
    </span>
  );
};
