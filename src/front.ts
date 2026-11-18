import type {Page} from "@shared/instrument";
import {rect, type Frame} from "@shared/surface";

export function marks(page: Page): Frame {
  if (page.fraction === undefined) return [];
  const count = Math.round(5 * Math.max(0, Math.min(1, page.fraction)));
  const cells: Frame = [
    rect("edge-top", 52, 5, 17, 1, "#889F9BFF"),
    rect("edge-bottom", 52, 14, 17, 1, "#889F9BFF"),
    rect("edge-left", 52, 6, 1, 8, "#889F9BFF"),
    rect("edge-right", 68, 6, 1, 8, "#889F9BFF"),
    rect("terminal", 69, 8, 2, 4, "#889F9BFF"),
  ];
  for (let i = 0; i < 5; i++) cells.push(rect("cell"+i, 54+i*3, 7, 2, 6, i<count?"#77DDA6FF":"#263B36FF"));
  return cells;
}
