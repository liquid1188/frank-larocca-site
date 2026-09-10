import { HtmlBasePlugin } from "@11ty/eleventy";
import fs from "node:fs";
import path from "node:path";
export default function (eleventyConfig) {
  eleventyConfig.addPlugin(HtmlBasePlugin);
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/admin": "admin", "src/assets": "assets", "src/images": "images", "src/scores": "scores", "src/CNAME": "CNAME" });
  eleventyConfig.addFilter("readableDate", (d) =>
    new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString());
  eleventyConfig.addFilter("shortDate", (iso) =>
    (typeof iso === "string" ? new Date(iso + "T12:00:00Z") : new Date(iso)).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("bySlug", (coll, slug) => coll.find((w) => w.data.slug === slug || w.fileSlug === slug));
  eleventyConfig.addFilter("ytid", (u) => (u || "").replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "").split("&")[0].split("?")[0]);
  eleventyConfig.addFilter("lvSort", (arr) => [...arr].sort((a, b) => (a.data.lvOrder || 99) - (b.data.lvOrder || 99) || a.data.title.localeCompare(b.data.title)));
  eleventyConfig.addFilter("urlencode", (v) => encodeURIComponent(v || ""));
  eleventyConfig.addGlobalData("today", () => new Date().toISOString().slice(0, 10));
  eleventyConfig.addGlobalData("buildId", () => Date.now().toString(36));
  eleventyConfig.addCollection("eventsSorted", (api) => api.getFilteredByTag("event").map((e) => ({
    iso: e.date.toISOString().slice(0, 10), work: e.data.title, time: e.data.time || "", venue: e.data.venue, city: e.data.city, who: e.data.who || "", url: e.data.url || ""
  })).sort((a, b) => a.iso.localeCompare(b.iso)));
  eleventyConfig.addFilter("longDate", (iso) => new Date(iso + "T12:00:00Z").toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric", timeZone: "UTC" }));
  // Home page news: posts and outside coverage merged, newest first
  eleventyConfig.addCollection("latestNews", (api) => {
    const posts = api.getFilteredByTag("news").map((p) => ({ year: p.date.getFullYear(), sort: p.date.getTime(), title: p.data.title, url: p.url, outlet: "" }));
    return posts;
  });

  // Responsive images: for every local raster <img>, attach the WebP variants generated in src/images
  // (same photos, served at the size each screen can show; never below 2x display width).
  const variantCache = new Map();
  function variantsFor(src) {
    if (variantCache.has(src)) return variantCache.get(src);
    const m = src.replace(/[?#].*$/, "").match(/^\/images\/(.+)\.(jpe?g|png)$/i);
    let out = null;
    if (m) {
      const dir = path.join("src/images", path.dirname(m[1]));
      const stem = path.basename(m[1]);
      let files = [];
      try { files = fs.readdirSync(dir); } catch {}
      const ws = files.map((f) => { const mm = f.match(new RegExp("^" + stem.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "-(\\d+)\\.webp$")); return mm ? +mm[1] : null; }).filter(Boolean).sort((a, b) => a - b);
      if (ws.length) out = ws.map((w) => `/images/${path.dirname(m[1]) === "." ? "" : path.dirname(m[1]) + "/"}${stem}-${w}.webp ${w}w`).join(", ");
    }
    variantCache.set(src, out);
    return out;
  }
  eleventyConfig.addTransform("responsive-images", function (content) {
    if (!(this.page.outputPath || "").endsWith(".html")) return content;
    return content.replace(/<img\b([^>]*)>/g, (tag, attrs) => {
      if (/\bsrcset=/.test(attrs)) return tag;
      const sm = attrs.match(/\bsrc="([^"]+)"/);
      if (!sm) return tag;
      const srcset = variantsFor(sm[1]);
      if (!srcset) return tag;
      let a = attrs + ` srcset="${srcset}"`;
      if (!/\bsizes=/.test(a)) a += ` sizes="(max-width: 900px) 100vw, 50vw"`;
      if (!/\bloading=/.test(a) && !/\bfetchpriority=/.test(a)) a += ` loading="lazy"`;
      if (!/\bdecoding=/.test(a)) a += ` decoding="async"`;
      return `<img${a}>`;
    });
  });
  return { dir: { input: "src", includes: "_includes", output: "_site" } };
}
