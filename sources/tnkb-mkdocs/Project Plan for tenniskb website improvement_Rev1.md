Project Plan for tenniskb website improvement

Currently, I have a github repo of tennisknowledgebase here C:\Users\Henry\Documents\Github\tennisknowledgebase which is the unfinished project from my other PC. I have a folder C:\Users\Henry\Downloads\Tenniskb\new-documents including all latest documents that I want to build a site and later publish to the unfinished github repo C:\Users\Henry\Documents\Github\tenniskb. You decide how to complete the project with following requirements

1. The reader can easily navigate the site and get the contents within 3 clicks, not more, so generate a navigation menu to do that.

2. The content must be easy to understand and do not write with many AI slops, not many indent or bullets or bold or icons like ChatGPT.

3. The materials must be grounded in the raw data files and do not allow any hallucination, remove them if there are in the raw documents.

4. In English files in side /en folders, there must be no Vietnamese phrases and words. Remove all of them and clean the page as a natural writing.

4. The new site content only come from C:\Users\Henry\Downloads\Tenniskb\new-documents and use the old site theme, color and introduction with tennis terms in Vietnamese. See this site as a reference for navigation structures.:  [Tai Chi Knowledge Base](https://henryphamduc.github.io/taichiknowledgebase/en/index.html) and [Trang Chủ - Tai Chi Knowledge Base](https://henryphamduc.github.io/taichiknowledgebase/vi/index.html) 

* * *

The GitHub repo at `C:\Users\Henry\Documents\Github\tenniskb` is the unfinished skeleton (empty docs/en, docs/vi, only mkdocs.yml and an empty theme folder). The Downloads folder is a goldmine — it has all the raw bilingual (EN/VI) coach-voice source documents. Before I do anything, let me load the relevant skill and plan this out.

The user has a tenniskb site already partially set up. Let me look at what's in the existing Github skeleton, then check the previous (July 2026) tenniskb session to understand the established conventions before doing anything.

The skeleton has nav structure (Foundation / Advanced / Elite, each with Overview + Basics + Deep Dives) but no content. The Downloads folder is the source. Let me look at the existing partials, CSS, and the existing index.md to understand the established patterns. Then I'll plan the menu structure from the raw documents.



The user wants me to publish the Downloads content to the Github skeleton, but with a different nav structure than the current skeleton. The skeleton is too generic (3 levels × 3 sub-sections = 9 stub pages, but there are 22 actual topic folders). I need to:

1. Build a proper navigation that lets the reader reach any topic in 3 clicks
2. Copy content from Downloads → Github (preserving "coach voice", stripping AI slop)
3. Verify nothing hallucinates from the raw source


