// Defaults for every work so the editor only needs the musical facts.
export default {
  layout: "work.njk",
  tags: ["work"],
  eleventyComputed: {
    slug: (data) => data.slug || data.page.fileSlug,
    permalink: (data) => data.permalink || `/works/${data.slug || data.page.fileSlug}/`,
  },
};
