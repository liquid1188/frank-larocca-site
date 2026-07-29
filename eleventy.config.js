export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/admin": "admin" });
  eleventyConfig.addFilter("readableDate", (d) =>
    new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })
  );
  return { dir: { input: "src", includes: "_includes", output: "_site" } };
}
