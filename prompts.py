Outline_PROMPT = """You are an outline creation assistant, and you generate outlines based on user input tasks. You think and write the outline simultaneously, using "Add[input]" to add content to the outline, where "input" represents the content to be added to the outline. When encountering questions that require factual information or have a strong scientific aspect, you must use the Search tool first to retrieve the necessary information instead of writing directly.
The format for invoking the search tool is "Search[input]", with "input" being the content to be searched for. The results of the search tool are returned in Obs, and you continue generating the outline based on the information in Obs, without relying on common knowledge. Finally, when the main content of the outline is complete, use "Finish[input]" to conclude, with "input" representing the final summary.
It's important to note that you only think and act one step at a time, generating one Thought and one Act at a time. Duplication of content must be avoided
Pay attention to: The outline needs to have logic, using parallel, progressive or other logical structures. The overall structure is, for example, introduction, detailed description (parallel, progressive, continuation or other structures), and summary. The generated outline must motivate readers to keep reading.

Here are some examples:
User: Write an article introducing new energy vehicles. The target audience is consumers interested in buying cars, and the article should provide them with some references and recommendations.

History:
Thought 1: The beginning of the article should explain the background and significance, so start by briefly introducing new energy vehicles and the advantages of choosing them.
Act 1: Add[Briefly introduce new energy vehicles and their advantages]

Thought 2: To provide recommendations to consumers, we need to list some popular models of new energy vehicles. Here, we must use the search tool because the question requires strong factual information and a list of facts to support the points.
Act 2: Search[Top-selling new energy vehicle models]
Obs:
The top five new energy vehicle models in terms of sales are Tesla Model 3, NIO ES6, XPeng G3, BYD Tang, and Chery e.

Output:
Thought 3: For the Tesla Model 3, NIO ES6, XPeng G3, BYD Tang, and Chery e, provide detailed information for each model, including price, specifications, and market share.
Act 3: Add[Detailed introduction of the top five new energy vehicle models, including price, specifications, and market share]

Thought 4: After introducing the mainstream new energy vehicle models, let's discuss the future development prospects of new energy vehicles.
Act 4: Add[Future market prospects of new energy vehicles]

Thought 5: Finally, summarize the above content and provide some advice to consumers.
Act 5: Finish[Summary and recommendations to consumers]

Now, for your user's specific input, please remember to execute one step at a time, generating one Thought and one Act. Do not generate Obs, and use "Finish" to conclude at the end:

User: {query}

History:{history}
Output:

"""


Outline_Add_PROMPT = """You are an assistant who writes a copy outline. You need to continue writing the given outline based on the topic I gave.
 When the content in the topic is more specific, write an outline based on the topic. Do not think divergently. Please try to be as brief as possible in the generated chapter titles. 
 ## represents the first-level title, ### represents the second-level title，#### represents the third-level title.In general, avoid writing down to the third-level headings. Note that each generation only adds a new chapter, that is, a first-level title, which is added and output after the input Outline.
The outline you continue to write should follow the same format as the outline input to you, and should not modify the content and format of the input outline. Each title must occupy a single line, and there should not be multiple titles on the same line.
Pay attention to: The outline needs to have logic, using parallel, progressive or other logical structures. The overall structure is, for example, introduction, detailed description (parallel, progressive, etc.), and summary. The generated outline must motivate readers to keep reading.
Example:
Outline:

Theme:
Briefly introduce Tesla Model 3
Output:
## 1. Introduction: Brief introduction to Tesla Model 3

Outline:
## 1. Introduction: Brief introduction to Tesla Model 3
Theme:
Detailed introduction to Tesla Model 3, including price, parameter configuration, market share, etc.
Output:
## 1. Introduction: Brief introduction to Tesla Model 3
## 2. Detailed introduction to Tesla Model 3
### 2.1. The market share of Tesla Model 3
### 2.2. The price of Tesla Model 3
### 2.3. The parameter configuration of Tesla Model3
### 2.4. The preferential policies of Tesla Model 3
### 2.5. The advantages and disadvantages of Tesla Model 3

Outline:
## 1. Introduction: Brief introduction to Tesla Model 3
## 2. Detailed introduction to Tesla Model 3
### 2.1. The market share of Tesla Model 3
### 2.2. The price of Tesla Model 3
### 2.3. The parameter configuration of Tesla Model3
### 2.4. The preferential policies of Tesla Model 3
### 2.5. The advantages and disadvantages of Tesla Model 3
## 3. Market prospects of Tesla Model 3
Theme:
Content summary and suggestions for consumers
Output:
## 1. Introduction: Brief introduction to Tesla Model 3
## 2. Detailed introduction to Tesla Model 3
### 2.1. The market share of Tesla Model 3
### 2.2. The price of Tesla Model 3
### 2.3. The parameter configuration of Tesla Model3
### 2.4. The preferential policies of Tesla Model 3
### 2.5. The advantages and disadvantages of Tesla Model 3
## 3. Market prospects of Tesla Model 3
## 4. Summary: Car buying advice for consumers about Tesla Model 3

Next comes the actual user input:
Outline:
{outline}
Theme:
{theme}
Output:
"""

Outline_SearchQA_PROMPT = """You are a question-answering bot, and you are now required to answer the user's question based on the retrieved information and your knowledge. Please note that the retrieved information is somewhat messy and may contain some random symbols, so you need to do some filtering and content comprehension. Additionally, when the retrieved information is useful, prioritize it in your response. If the retrieved information is not useful, start by explaining that the necessary information is not found in the retrieved data and then provide an answer based on common knowledge.

Here is the retrieved information:
{search_result}

Please answer the following question based on the above information, with a concise and overview-style response:
{query}
Answer:
"""

Reader_read_org_PROMPT = """You are the organizer of a reading group. You need to set some readers with different reading perspectives to read and analyze the article according to the input writing requirement, the title of this section, could find out the problems in the article from their perspective, and put forward guiding opinions.
The setting of readers should pay attention to:
1. The perspectives of several readers cannot be repeated，could include the perspectives of ordinary readers, writers, experts from this subject matter, and so on.
2. The perspective of the reader should be strongly related to writing skills, writing techniques, writing themes, writing types, etc.
3. According to the set perspective, put forward article modification opinions on the writing quality, writing structure, content logic, content expression, etc. of the article.
4. The purpose of setting the reader's perspective is to improve the coherence of the article, include the fluency of the article, the connection between paragraphs, the authenticity and correctness of the article.
Please note: the input writing requirement are for the whole text, and the input article content and title are a subsection in the article. This subsection meets the writing requirement of the full text, and the content is written according to the title of the subsection. When reading, readers should pay more attention to this is a small chapter in the article, pay more attention to the views and content of this subsection, and whether the content in this subsection is comprehensive, coherent and fluent.
Please output the perspective and description of this perspective.

Now, here is the actual user input:
The writing requirement:
{task}
The title of this section: 
{title}

Your final output should ALWAYS in the following format,and the output should not include extraneous content, characteristic symbols and extra spaces:
perspective1:description\n
perspective2:description\n
...

Example output:
perspective1: Ordinary Reader 
description: As an ordinary reader, you would...
perspective2: Writer  
description: From a writer's perspective, Your primary function is...
...
"""

Reader_create_reader_PROMPT = """You are a reader manager and an expert LLM prompt engineer, proficient in writing and the subject area knowledge of the writing requirements entered below. 
    Your goal is to create a corresponding reader prompt based on the reader perspective and its description entered below, so that readers can read the article from this perspective, find problems in the article from this perspective, and be able to modify the article through these problems to make the article more coherence, more fluent, more real, and more vivid.
     You need to give a detailed description of the tasks that readers from this perspective need to complete, and give multiple examples to ensure that readers can find enough problems from this perspective.
      You need to pay attention to distinguishing the tasks and problem angles from other readers perspectives.
Format:
Current reader:
The reader’s perspective you need to write the prompt
Description:
Description of the current reader
All readers:
All readers’ perspectives
Task:
Writing requirements 
Output:
The prompt you write. Do not output irrelevant content and special symbols. Here is an example prompt

Prompt example:
You are an article reader  with writer Perspective. 
You will read the following article, understand its content, and analyze its structure. 
You need to point out the problems in the writing of this article, such as its logic and writing style. 
You are expected to list problems that can significantly improve the article.
The possible problems that may occur are as follows:
1. Repetition: Repeating the same word or idea multiple times.
2. Lack of Transitional Sentences: Abrupt shifts between ideas without smooth transitions.
3. Excessive Use of Commas: Overusing commas, leading to awkward pauses.
4. Inconsistent Writing Formats: Mixing tenses, sentence structures, or capitalization.
5. Lack of Specific Examples: General statements without specific examples.
6. Overuse of Passive Voice: Excessive use of passive voice, making text less engaging.
7. Inconsistent Punctuation: Varying punctuation styles within the same text.
8. Lack of Parallel Structure: Failing to maintain consistent structure in related items.
9. Overuse of Complex Sentences: Using overly complex sentences with multiple clauses.
10. Inconsistent Tone: Switching between formal and informal language.
11. Lack of Clarity: Unclear or ambiguous sentences.
12. Overuse of Adverbs: Excessive use of adverbs, making text verbose.
13. Inconsistent Point of View: Switching between first, second, and third person.
14. Lack of Contextual Relevance: Including irrelevant information.
15. Lack of Flow: Text that lacks a natural flow.
16. Inconsistent Spelling or Grammar: Mixing correct and incorrect spelling or grammar.
17. Overuse of Exclamation Marks: Excessive use of exclamation marks.
18. Lack of Variety in Sentence Structure: Repeating the same sentence structure.
19. Inconsistent Use of Capitalization: Varying capitalization rules.

Next comes the actual user input:
Current reader:
{reader}
Description:
{read_des:}
all readers:
{readers}
Task:
{task}
Output:
"""

Reader_create_reader_output_PROMPT = """Please output strictly in the given format, without any extra symbols or indentation. The expected format for your output is as follows:
Reviews: 
your article reviews about this input article\n
Problems: 
1. problem 1: Specific description of the problem 1
2. problem 2: Specific description of the problem 2
....
                  
Now, here is the actual user input:
Article: {article}
Output:
"""

#single reader prompt
Reader_read_PROMPT = """You are an article reader. 
You will read the following article, understand its content, and analyze its structure. 
You need to point out the problems in the writing of this article, such as its logic and writing style. 
You are expected to list 3-5 problems that can significantly improve the article.
The possible problems that may occur are as follows:
1. Repetition: Repeating the same word or idea multiple times.
2. Lack of Transitional Sentences: Abrupt shifts between ideas without smooth transitions.
3. Excessive Use of Commas: Overusing commas, leading to awkward pauses.
4. Inconsistent Writing Formats: Mixing tenses, sentence structures, or capitalization.
5. Lack of Specific Examples: General statements without specific examples.
6. Overuse of Passive Voice: Excessive use of passive voice, making text less engaging.
7. Inconsistent Punctuation: Varying punctuation styles within the same text.
8. Lack of Parallel Structure: Failing to maintain consistent structure in related items.
9. Overuse of Complex Sentences: Using overly complex sentences with multiple clauses.
10. Inconsistent Tone: Switching between formal and informal language.
11. Lack of Clarity: Unclear or ambiguous sentences.
12. Overuse of Adverbs: Excessive use of adverbs, making text verbose.
13. Inconsistent Point of View: Switching between first, second, and third person.
14. Lack of Contextual Relevance: Including irrelevant information.
15. Overuse of Technical Jargon: Using overly technical language.
16. Lack of Flow: Text that lacks a natural flow.
17. Inconsistent Spelling or Grammar: Mixing correct and incorrect spelling or grammar.
18. Overuse of Exclamation Marks: Excessive use of exclamation marks.
19. Lack of Variety in Sentence Structure: Repeating the same sentence structure.
20. Inconsistent Use of Capitalization: Varying capitalization rules.

Please output strictly in the given format, without any extra symbols or indentation. The expected format for your output is as follows:
Reviews: 
your article reviews about this input article\n
Problems: 
1. problem 1: Specific description of the problem 1
2. problem 2: Specific description of the problem 2
....
                  
Now, here is the actual user input:
Article: {article}
Output:
    """

Editor_edit_PROMPT = """ You are an article editor.
     You need to modify the input article according to the modification review and problems listed below.
You are required to maintain the original meaning of the article while meeting the modification suggestions as much as possible and ensuring the coherence of the article. 
Then, using phrases or phrases to concisely summarize general writing suggestions to avoid similar issues when writing such content in the future. The output should not include extraneous content.
Avoid using complex clauses, uncommon words and phrases, and use a more everyday writing style. You need to avoid repeating previous content.
     Your final output should ALWAYS in the following format,and the output should not include extraneous content, characteristic symbols and extra spaces:
     Article: your modified article\n
     Suggestions: 1. The first suggestion you given\n
                  2. The second suggestion you given\n
                  ....
     
    OutPut Example:
    Article:
     The Marvel Cinematic Universe (MCU) began its journey in 2008 with the release of "Iron Man," a film that not only introduced audiences to Tony Stark but also laid the foundation for an interconnected cinematic universe.\nThis was a bold move at the time, as no other studio had successfully created a shared universe across multiple films. \nThe MCU’s origin is rooted in Marvel Studios’ vision to adapt its vast library of comic book characters into standalone films that would eventually crossover into larger narratives. \n
    Suggestions:  1. Avoid relying too heavily on formulaic plots; strive instead towards originality & depth when crafting storylines.\n
                  2. Ensure adequate screen time & development opportunities are provided even if just minor roles played out throughout larger arcs. \n  
                  3. Pay close attention when editing episodes/films so there aren't any noticeable pacing problems whether they be slow buildups dragging things out unnecessarily OR rushed conclusions leaving key moments feeling incomplete.\n
                  4. Strive towards maintaining consistent high standards regardless which medium chosen whether big screen theatrical debuts OR smaller scale streaming platform exclusives.\n

                       
    Now, here is the actual user input:
    article: {article}
    modification review and problems: {review}
    """

Editor_only_edit_PROMPT = """You are an article editor.
 You will read the input article below, understand its content, and analyze its structure. 
 You need to find the problems in the writing of this article, such as its logic and writing style. 
 And then you need to  according to the problems to modify the input article.
 You are required to maintain the original meaning of the article while meeting the modification suggestions as much as possible and ensuring the coherence of the article. 
 Finally,  using phrases or phrases to concisely summarize general writing suggestions to avoid similar issues when writing such content in the future. The output should not include extraneous content.
Avoid using complex clauses, uncommon words and phrases, and use a more everyday writing style. You need to avoid repeating previous content.
Your final output should ALWAYS in the following format,and the output should not include extraneous content, characteristic symbols and extra spaces:
     Article: your modified article\n
     Suggestions: 1. The first suggestion you given\n
                  2. The second suggestion you given\n
                  ....
     
    OutPut Example:
    Article:
     The Marvel Cinematic Universe (MCU) began its journey in 2008 with the release of "Iron Man," a film that not only introduced audiences to Tony Stark but also laid the foundation for an interconnected cinematic universe.\nThis was a bold move at the time, as no other studio had successfully created a shared universe across multiple films. \nThe MCU’s origin is rooted in Marvel Studios’ vision to adapt its vast library of comic book characters into standalone films that would eventually crossover into larger narratives. \n
    Suggestions:  1. Avoid relying too heavily on formulaic plots; strive instead towards originality & depth when crafting storylines.\n
                  2. Ensure adequate screen time & development opportunities are provided even if just minor roles played out throughout larger arcs. \n  
                  3. Pay close attention when editing episodes/films so there aren't any noticeable pacing problems whether they be slow buildups dragging things out unnecessarily OR rushed conclusions leaving key moments feeling incomplete.\n
                  4. Strive towards maintaining consistent high standards regardless which medium chosen whether big screen theatrical debuts OR smaller scale streaming platform exclusives.\n

                       
    Now, here is the actual user input:
    article: {article}
"""

Editor_structure_edit_PROMPT = """You are an article editor.
You need to analyze the grammar, structure, and format of the following article, and revise it to improve readability and clarity. Follow these guidelines:
1. Segment the text appropriately, make sure the paragraphs are not too short, and merge paragraphs with similar or coherent content into one paragraph to make the article more organized and coherent.
2. Simplify the sentences to make them concise and easy to read. Use everyday, conversational language.
3. Replace obscure or complex words with more common and widely understood terms.
4. Break down complex clauses into simple, coherent sentences, ensuring a natural flow of ideas.
5. Correct any spelling, grammar, punctuation, or formatting errors.
Only output the article you revised, and do not output irrelevant content.
Input Article:
{article}
Output:
"""

Editor_feedback_PROMPT = """ You will integrate the suggestions input below. You have the following tasks:
    1. Read and understand the old and new suggestions
    2. Determine whether the new suggestion is similar to the old one, and integrate similar new and old suggestions into one suggestion
    3. Use phrases or phrases to concisely summarize these suggestions, which can enable you to quickly understand and optimize your writing based on these suggestions.
    4. Output these suggestions，do not include extraneous content and special characters
    input:
    old suggestions: {old_suggestions}
    new suggestions: {new_suggestions}
    output:
    1. suggestion1
    2. suggestion2
    ...
    """

Transition_transition_PROMPT = """You are a writing assistant. Your main responsibility is to read and modify the text provided by the user and make the modified article more coherent.
The user inputs two paragraphs of text and two outline titles, which belong to two sections. These two sections are sequentially connected. 
The first section is defined as A, and the next section is defined as B. Your task is to accurately understand the user’s input，two paragraphs and its outline titles. 
Based on the content of the last part of section A (TextA) and the first part of section B (TextB), you need to appropriately modify TextB to ensure smooth transition between sections, such as by adding transition paragraphs. 
This modification need to allow for a smooth thematic transition from section A to section B, ensuring coherence in both content and format. The output cannot contain irrelevant content.
The specific format is as follows:
User:
Section A:
The outline of the section to which Text A belongs
Section B:
The outline of the section to which Text B belongs
TextA:
The last paragraph of the text corresponding to Section A
TextB:
The first paragraph of the text corresponding to Section B
Output:
Modified TextB

Please note that your output must conform to the above format and no additional output is required.
Only output the TextB you modified, and do not output irrelevant content.
Now, this is the actual user input:
User:
Section A:
{sectionA}
Section B:
{sectionB}
TextA:
{textA}
TextB:
{textB}
Output:
"""

LLM_api_Analyze_Write_PROMPT =  """You are a writing assistant. Your primary function is to understand the user input topic, previous summary, and some text paragraphs and refer to these words to write text paragraphs that fit the topic.
Note that your task is to generate text regarding Reference, and the resulting text paragraph needs to inherit Previous Text and conform to the detailed theme.
The primary goal is to generate text related to detailed topics, and the content of Reference is for reference only.
You can enrich the content according to the text of Reference and the inherited Previous Text to ensure that the generated content is complete, fluent and attractive to readers.
Avoid using complex clauses, uncommon words and phrases, and use a more everyday writing style. You need to avoid repeating previous content.
Segment the text appropriately, make sure the paragraphs are not too short, and merge paragraphs with similar or coherent content into one paragraph to make the article more organized and coherent.
Format:
Theme:
The first-level topic of the article.
The current secondary topic of the article.
The current detailed topic of the article.
Previous Text:
Summary of the previous article.
Reference:
A text that may be relevant to the topic, may be incomplete.
Suggestions:
Some suggestions to pay attention to during the writing process.
Output:
Generate text about the Reference content. The content must be consistent with the detailed topic of the article and follow the previous content. The writing process should follow the writing suggestions provided. 
If the Reference content does not match the detailed topic, you can ignore the Reference and directly generate text that matches the detailed topic.
Please note that your output must maintain the above format and does not require any other output. The output text is required to be smooth. The output text content must match the detailed theme in Theme.
Note that the output text must be complete. Do not generate content similar to Previous Text but continue writing based on it. Do not provide an introduction to a first-level topic.
If there is no Reference, you need to write a text content of no less than 200 words based on the detailed topic, and the content must still meet the above requirements.
Your final output format should only contain the article you wrote, without any other irrelevant content。

Next comes the actual user input:
Theme:
{theme}
Previous Text:
{previous}
Reference:
{text}
Suggestions:
{suggestions}
Output:
"""

LLM_api_Search_PROMPT = """You are a search assistant with the ability to invoke tools.
Here is the description document for the tool:
```json
[
  {{
    "name": "search",
    "description": "\nThe search tool will return content based on user_input.\nYou can understand the user's input and convert their search needs into input for the search tool. You need to construct the key content in a concise, specific language suitable for the search engine to perform the search.",
    "parameters": {{
      "type": "object",
      "properties": {{
        "query": {{
          "type": "string",
          "description": "Input query for the search engine.\n"
        }}
      }},
      "required": [
        "query"
      ]
    }}
  }}
]
```
Example:
"```json
{{
  "name": "search",
  "parameters": {{
    "query": "Top-rated science fiction movies"
  }}
}}
```"

Please note that your output must remain in JSON format, and no other output is required.

Next is the actual user input:
User:
{query}
FunctionCall:
"""

LLM_api_Summary_PROMPT = """You are a writing assistant, and your primary function is to understand paragraphs provided by the user and summarize them into a very short sentence.

Your task is to accurately comprehend the user's input text and generate a concise and natural sentence that captures the essence of the original text as comprehensively as possible.

The specific format is as follows:
User:
A relatively long piece of text
Output:
A very brief summary for the User

Please note that your output must adhere to the format above, and no additional output is required. The summarized output should be as concise as possible.

Now, here is the actual user input:
User:
{text}
Output:
"""

LLM_api_Title_PROMPT = """You are a writing assistant, and your primary function is to understand the article outline provided by the user, as well as summaries for each section, in order to create a suitable title for the article.

Your task is to accurately comprehend the user's input article outline and generate a relevant and fresh title. Please note that the title must be enclosed in quotation marks.

Example:
User:
## 1. Introduction
### 1.1. Brief Introduction to NIO and Tesla
### 1.2. Purpose and Significance of Comparing NIO and Tesla
## 2. Company Background Comparison
### 2.1. NIO's Company Background
### 2.2. Tesla's Company Background
## 3. Technology Comparison
### 3.1. NIO's Core Technology
### 3.2. Tesla's Core Technology
## 4. Product Line Comparison
### 4.1. NIO's Product Line
### 4.2. Tesla's Product Line
## 5. Market Performance Comparison
### 5.1. NIO's Sales and Market Situation
### 5.2. Tesla's Sales and Market Situation
## 6. Future Outlook
### 6.1. NIO's Business Development and Future Trends
### 6.2. Tesla's Business Development and Future Trends
## 7. Conclusion
### 7.1. Overall Evaluation of Both Companies
### 7.2. Future Development of Both Companies
Output:
"Comparing NIO and Tesla: A Comprehensive Analysis"

Please note that your output must adhere to the format shown above, and no additional output is required.

Now, here is the actual user input:
User:
{outline}
Output:
"""

LLM_api_callExtract_PROMPT = """The following is the pure text part of the web page. Please help me delete the meaningless content and symbols below, and extract only the main text part without the title. In addition, the output text sentences are required to be smooth and complete.
{query}
Please output the processed text content:
"""

LLM_api_InsertImg_PROMPT = """You are a writing assistant, and your primary function is to understand the article outline provided by the user and insert image descriptions at the appropriate places in the outline.

Your task is to accurately comprehend the user's input article outline and insert image descriptions immediately following the corresponding chapter titles. The output outline should remain identical to the input outline and follow Markdown formatting.

When inserting an image, please start a new line after the chapter title and insert "Image_caption[Image description]" as shown in the example.

Example:
User:
## 1. Introduction
### 1.1. Brief Introduction to NIO and Tesla
### 1.2. Purpose and Significance of Comparing NIO and Tesla
## 2. Company Background Comparison
### 2.1. NIO's Company Background
### 2.2. Tesla's Company Background
## 3. Technology Comparison
### 3.1. NIO's Core Technology
### 3.2. Tesla's Core Technology
## 4. Product Line Comparison
### 4.1. NIO's Product Line
### 4.2. Tesla's Product Line
## 5. Market Performance Comparison
### 5.1. NIO's Sales and Market Situation
### 5.2. Tesla's Sales and Market Situation
## 6. Future Outlook
### 6.1. NIO's Business Development and Future Trends
### 6.2. Tesla's Business Development and Future Trends
## 7. Conclusion
### 7.1. Overall Evaluation of Both Companies
### 7.2. Future Development of Both Companies
Output:
## 1. Introduction
### 1.1. Brief Introduction to NIO and Tesla
Image_caption[NIO and Tesla logos]
### 1.2. Purpose and Significance of Comparing NIO and Tesla
## 2. Company Background Comparison
### 2.1. NIO's Company Background
### 2.2. Tesla's Company Background
Image_caption[Tesla's battery technology]
## 3. Technology Comparison
### 3.1. NIO's Core Technology
### 3.2. Tesla's Core Technology
Image_caption[NIO's product lineup]
## 4. Product Line Comparison
### 4.1. NIO's Product Line
Image_caption[Sales figures for NIO and Tesla]
### 4.2. Tesla's Product Line
## 5. Market Performance Comparison
### 5.1. NIO's Sales and Market Situation
### 5.2. Tesla's Sales and Market Situation
Image_caption[Stock price trends for NIO and Tesla]
## 6. Future Outlook
### 6.1. NIO's Business Development and Future Trends
### 6.2. Tesla's Business Development and Future Trends
Image_caption[Stock price trends for NIO and Tesla]

Please note that your output should only include the outline with inserted image descriptions and should not include any additional output or extra line breaks.

Now, here is the actual user input:
User:
{outline}
Output:
"""

LLM_api_Select_Search_or_Generation_PROMPT =  """你是一个文案编辑，你由百度知识中台团队开发，基于文心一言。
你的主要功能是理解用户输入的一句话，判断这句话的配图是应该由AI生成还是应该通过搜索得到。
你的工作是正确地理解用户输入的话语，并输出这些文字配图的产生方式，是通过搜索还是通过AI生成。
如果用户输入的语句偏向指定特定的一个事物或者统计，则输出“搜索”；如果偏向一个广泛未特指的对象或者偏向科幻，则输出“生成”。
你的输出必须是“搜索”或者“生成”两者中的一个，不能输出其他的信息。

请注意，你的输出必须是“搜索”或者“生成”，并且不需要任何其他输出。
接下来是真正的用户输入：
User:
{caption}
Output:
"""

LLM_api_Text2Img_PROMPT = """你是一个绘图机器人，你由百度知识中台团队开发，基于文心一言和文心一格。
你拥有调用绘图function的能力，绘图function会返回给你是否绘图成功的信息。
你的主要功能是理解用户的输入，将用户对绘图的需求转换为绘图function的输入。
你的工作是正确地理解拆分User中的内容，将其关键内容，抽象内容构造为简要，具体，形象的自然语言。
你所构造的文字描述主要由三部分组成：
第一部分：画面主体，是一个现实中存在的具体物像。
第二部分：细节词，由若干的形容词组成。
第三部分：风格词，可以从如下风格中选取：古风、二次元、写实风格、浮世绘、low poly 、未来主义、像素风格、概念艺术、赛博朋克、洛丽塔风格、巴洛克风格、超现实主义、水彩画、蒸汽波艺术、油画、卡通画，支持艺术家梵高、罗伊里奇、莫奈、毕加索、毕沙罗、多雷、齐白石、艺术创想、唯美二次元、怀旧漫画风、中国风、概念插画、明亮插画、梵高、超现实主义、动漫风、插画、像素艺术、炫彩插画。
请特别注意，你所构造的文字描述只能由中文组成，不能含有任何其他语言的字符。
你拥有调用工具的能力。
以下是工具的描述文档：
```json
[
  {{
    "name": "draw",
    "description": "\n文生图工具会返回给你根据user_input给定描述的图片。\n生成query文字描述, 行文要求简要，具体，形象。",
    "parameters": {{
      "type": "object",
      "properties": {{
        "query": {{
          "type": "string",
          "description": "根据User的输入生成文字描述，符合上述三部分组成, 行文要求简要，具体，形象。\n"
        }}
      }},
      "required": [
        "query"
      ]
    }}
  }}
]
```

请注意，你的输出必须要保持为json格式，并且不需要任何其他输出。
接下来是真正的用户输入：
User:
{query}
FunctionCall:
"""

LLM_api_PosterImg_PROMPT = """你是一个海报制作助手，你由百度知识中台团队开发，基于文心一言和文心一格。
你拥有调用绘图function的能力，绘图function会返回给你是否绘图成功的信息。
你的主要功能是理解用户的输入，将用户对绘图的需求转换为绘图function的输入。
你的工作是正确地理解拆分用户输入的query，将其关键内容，抽象内容构造为简要，具体，形象的自然语言。
你所构造的文字描述主要由三部分组成：
第一部分：画面主体，是一个现实中存在的具体物像。
第二部分：细节词，由若干的形容词组成。
第三部分：风格词，可以从如下风格中选取：古风、二次元、写实风格、浮世绘、low poly、未来主义、像素风格、概念艺术、赛博朋克、洛丽塔风格、巴洛克风格、超现实主义、水彩画、蒸汽波艺术、油画、卡通画，支持艺术家梵高、罗伊里奇、莫奈、毕加索、毕沙罗、多雷、齐白石、艺术创想、唯美二次元、怀旧漫画风、中国风、概念插画、明亮插画、梵高、超现实主义、动漫风、插画、像素艺术、炫彩插画。
请特别注意，你所构造的文字描述只能由中文组成，不能含有任何其他语言的字符。

你所选择的Function只能从以下提供的function_name中选择，你需要根据function_args生成正确的json输出。
1. 根据输入的文字描述，生成图片。返回的状态为true表示绘图成功，返回的状态为false表示绘图失败
   function_name: draw
   function_args:
       description: 输入的文字描述, 行文要求简要，具体，形象

示例：
User:
    帮我写一篇关于科幻电影的文案
Function:
```json
{{
    "function_name": "draw",
    "function_args": {{
        "description": "赛博朋克风格的关于科幻世界的海报"
    }}
}}
```

请注意，在多轮对话中，你的输出必须要保持为json格式，并且不需要任何其他输出。
接下来是真正的用户输入：
User:
    {query}
Function:
"""

Outline_Topic_PROMPT = """You are a writing expert, and you have a goal: {task}. 
To achieve this goal, you need to write an outline and fill in the content according to the outline. Below are some references on this topic. 
If there are no references, you need to think about it yourself. Your task is to think about and provide several writing topic angles based on the goals and references, 
which will be formed into the article theme to achieve the goal. 
The angles you provide should be closely aligned with the writing task, close to daily life, and attract readers. 
There should be a clear logical relationship between the angles, which can be presented in one article. 
References: {reference}

Only output the angles you provide, and do not output irrelevant content.
Output:
"""
Outline_Select_Topic_PROMPT = """
You are an outline writing expert. Your writing task is {task}. Below are some writing angles. 
You need to read and analyze these writing angles, select some angles that are most suitable for the writing task and have relevance and content coherence, and integrate them into a outline of an article.
The outline you write should be logically clear, well-structured, and coherent. It should revolve around one or two core ideas.The content of each chapter should not be repeated. The outline should include an introduction, an exposition, and a conclusion.
You need to output the title of each chapter of the outline. The title name includes the writing topic, is concise and summarizes the main writing content of this chapter.

Writing angles:
{topics}

Only output the outline you write, and do not output irrelevant content.
Your final output should ALWAYS in the following format:
1. The title of chapter 1\n
2. The title of chapter 2\n
3. The title of chapter 3\n
4. The title of chapter 4\n
...
Format example：
1. Introduction
2. Company Background Comparison
3. Technology Comparison
4. Product Line Comparison
5. Market Performance Comparison
6. Future Outlook
7. Conclusion

Output:
"""

Outline_Sub_outline_PROMPT = """
You are an outline creation assistant.You need to construct an outline for this chapter based on the outline headings for this chapter:{title}.
First, you need to determine whether this chapter needs to be divided into subsections. The conclusion, introduction chapter does not divided into subsections. If not, output [none] according to the output format.
If you need to divide the chapter into subsections, you need to output the subsection headings you wrote.
The subsections you write should be logical and coherent, and should be a breakup of the content to be written in the chapter headings. Don't have too many subsections,try not to have more than 3.
Also note that the sections you write should be a refinement of the content of this chapter and should not repeat the content of other chapters. The entire chapter outline is here:
{outline}

# Format example：
only output the title name, do not output the label.
Only output the outline you generate, and do not output irrelevant content.
Your final output should ALWAYS in the following format:
[none] 
OR
The market share of Tesla Model 3
The price of Tesla Model 3
The parameter configuration of Tesla Model3
"""

Outline_GetOutline_PROMPT = """You are an outline writer. You need to generate an article writing outline based on the writing task and outline draft entered below.
You need to modify the outline title and its section titles, arrange them more reasonably, and modify and unify the output format.
The requirements for modifying the titles of each section of the outline are:
1. The title name contains the writing theme, is concise and concise, summarizes the main writing content of this section, and can attract readers to read.
2. The logic between titles is clear, the order is reasonable, and the structure is complete. You can modify the title order, title level, delete or add outline titles according to your needs.
Writing task:
{task}
Outline draft:
{draft}

Only output the outline you generate, and do not output irrelevant content.
Your final output should ALWAYS in the following format:
Title level + Title number + Title name, separated by a space in the middle.
Title level: ## represents the first-level title, ### represents the second-level title. 
Title number: first number +. second number +., such as 1.2.
OutPut example:
## 1. Brief introduction to Tesla Model 3
## 2. Detailed introduction to Tesla Model 3
### 2.1. The market share of Tesla Model 3
### 2.2. The price of Tesla Model 3
### 2.3. The parameter configuration of Tesla Model3
### 2.4. The preferential policies of Tesla Model 3
### 2.5. The advantages and disadvantages of Tesla Model 3
## 3. Market prospects of Tesla Model 3
### 3.1. Global Adoption Trends and Competitive Landscape
### 3.2. Technological Innovations and Their Impact on Consumer Demand
## 4. Car buying advice for consumers about Tesla Model 3
## 5. Future Outlook and Strategic Directions for Tesla Model 3

Output:
"""