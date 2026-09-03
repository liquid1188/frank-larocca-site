import { HtmlBasePlugin } from "@11ty/eleventy";
export default function (eleventyConfig) {
  eleventyConfig.addPlugin(HtmlBasePlugin);
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/admin": "admin", "src/assets": "assets", "src/images": "images" });
  eleventyConfig.addFilter("readableDate", (d) =>
    new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString());
  eleventyConfig.addFilter("shortDate", (iso) =>
    (typeof iso === "string" ? new Date(iso + "T12:00:00Z") : new Date(iso)).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("bySlug", (coll, slug) => coll.find((w) => w.data.slug === slug || w.fileSlug === slug));
  eleventyConfig.addFilter("ytid", (u) => (u || "").replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "").split("&")[0].split("?")[0]);
  eleventyConfig.addGlobalData("today", () => new Date().toISOString().slice(0, 10));
  eleventyConfig.addGlobalData("buildId", () => Date.now().toString(36));
  eleventyConfig.addCollection("eventsSorted", (api) => api.getFilteredByTag("event").map((e) => ({
    iso: e.date.toISOString().slice(0, 10), work: e.data.title, time: e.data.time || "", venue: e.data.venue, city: e.data.city, who: e.data.who || "", url: e.data.url || ""
  })).sort((a, b) => a.iso.localeCompare(b.iso)));
  eleventyConfig.addFilter("longDate", (iso) => new Date(iso + "T12:00:00Z").toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric", timeZone: "UTC" }));
  return { dir: { input: "src", includes: "_includes", output: "_site" } };
}
