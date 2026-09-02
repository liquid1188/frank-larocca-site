export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/admin": "admin", "src/assets": "assets", "src/images": "images" });
  eleventyConfig.addFilter("readableDate", (d) =>
    new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString());
  eleventyConfig.addFilter("shortDate", (iso) =>
    (typeof iso === "string" ? new Date(iso + "T12:00:00Z") : new Date(iso)).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" })
  );
  eleventyConfig.addFilter("bySlug", (coll, slug) => coll.find((w) => w.data.slug === slug || w.fileSlug === slug));
  eleventyConfig.addFilter("ytid", (u) => (u || "").replace("https://www.youtube.com/watch?v=", "").replace("https://youtu.be/", "").split("&")[0]);
  eleventyConfig.addGlobalData("today", () => new Date().toISOString().slice(0, 10));
  return { dir: { input: "src", includes: "_includes", output: "_site" } };
}
