"""Social Eagle Prompt Engineering Exam: question bank, answer key, rubrics and gamification.

Ported from Social_Eagle_Prompt_Exam.html. Edit questions here.

Rubric helpers:
  c(label, pts, pattern)                     -> award `pts` once if the pattern matches.
  k(label, pattern, each, cap, distinct)     -> award `each` per match, up to `cap` matches.
"""
from __future__ import annotations

from .models import Badge, Level, Question, Roast, Section, c, k

EXAM_TITLE = 'Prompt Engineering Exam'
EXAM_MINUTES = 90
TOTAL_MARKS = 100

SECTIONS: list[Section] = [
    Section('A', 1, 'RTCFR & Techniques', '20 MCQs · 1 mark each', 20),
    Section('B', 2, 'Short Answers', '15 questions · 2 marks each', 30),
    Section('C', 3, 'Write Prompts', '10 prompts · 3 marks each', 30),
    Section('D', 4, 'Identify RTCFR', '5 questions · 2 marks each', 10),
    Section('E', 5, 'Keyword Vault', '10 keywords · XP bonus only', 0),
]

QUESTIONS: list[Question] = [
    # ---------- Section A: RTCFR & Techniques ----------
    Question(n=1, sec='A', marks=1, type='mcq', q='What does RTCFR stand for?',
             opts=['Role, Task, Context, Few-shot, Response', 'Reasoning, Tool, Context, Format, Result', 'Role, Testing, Chain, Format, Response', 'Read, Think, Create, Final, Review'], ans=0),
    Question(n=2, sec='A', marks=1, type='mcq', q='In RTCFR, “Role” means:',
             opts=['The final answer format', 'The expert identity or perspective given to AI', 'The number of examples in the prompt', 'The user account type'], ans=1),
    Question(n=3, sec='A', marks=1, type='mcq', q='Which one is a strong Role prompt?',
             opts=['Tell me about marketing', 'Act as a senior digital marketing strategist', 'Give me answer fast', 'Make it better'], ans=1),
    Question(n=4, sec='A', marks=1, type='mcq', q='In RTCFR, “Task” means:',
             opts=['Background information', 'The exact work AI should perform', 'The output design only', 'A safety warning'], ans=1),
    Question(n=5, sec='A', marks=1, type='mcq', q='Which is the clearest Task statement?',
             opts=['AI', 'Explain AI agents', 'Create a 5-minute YouTube script explaining AI agents for Tamil business owners', 'Help me with content'], ans=2),
    Question(n=6, sec='A', marks=1, type='mcq', q='Context is important because:',
             opts=['It helps AI guess randomly', 'It reduces relevance', 'It gives background information and improves accuracy', 'It always makes the answer shorter'], ans=2),
    Question(n=7, sec='A', marks=1, type='mcq', q='Few-shot prompting means:',
             opts=['Giving one or more examples to guide the output', 'Asking AI to answer in one line', 'Asking AI to ignore examples', 'Giving only a role'], ans=0),
    Question(n=8, sec='A', marks=1, type='mcq', q='Response format in RTCFR means:',
             opts=['How the final output should be structured', 'The name of the AI model', 'The system speed', 'The number of users'], ans=0),
    Question(n=9, sec='A', marks=1, type='mcq', q='Which is an example of a response format instruction?',
             opts=['Act as a teacher', 'Give the output in table format', 'This is for students', 'Use the internet'], ans=1),
    Question(n=10, sec='A', marks=1, type='mcq', q='Prompt chaining means:',
             opts=['Writing one long prompt only', 'Splitting a big task into multiple connected prompts', 'Removing context from the prompt', 'Asking unrelated questions'], ans=1),
    Question(n=11, sec='A', marks=1, type='mcq', q='Sequential prompt chaining means:',
             opts=['Each step depends on the previous output', 'All agents debate each other', 'AI ignores previous answers', 'Prompt is written backward'], ans=0),
    Question(n=12, sec='A', marks=1, type='mcq', q='CoT stands for:',
             opts=['Chain of Thought', 'Code of Testing', 'Context of Tool', 'Create Output Template'], ans=0),
    Question(n=13, sec='A', marks=1, type='mcq', q='CoT prompting is mainly used for:',
             opts=['Step-by-step problem solving and reasoning', 'Image compression', 'File storage', 'Account login'], ans=0),
    Question(n=14, sec='A', marks=1, type='mcq', q='ToT stands for:',
             opts=['Task of Thinking', 'Tree of Thoughts', 'Tool of Testing', 'Tone of Text'], ans=1),
    Question(n=15, sec='A', marks=1, type='mcq', q='Tree of Thoughts prompting is useful when:',
             opts=['There are multiple possible solution paths', 'Only one-word answer is needed', 'No reasoning is needed', 'The answer must be random'], ans=0),
    Question(n=16, sec='A', marks=1, type='mcq', q='ReAct prompting combines:',
             opts=['Reasoning and Acting', 'Reading and Copying', 'Role and Task only', 'Response and Title'], ans=0),
    Question(n=17, sec='A', marks=1, type='mcq', q='ReAct prompting is useful for:',
             opts=['Tool-based workflows and agentic tasks', 'Only grammar correction', 'Only image design', 'Only translation'], ans=0),
    Question(n=18, sec='A', marks=1, type='mcq', q='Multi-agent prompting means:',
             opts=['One AI gives one answer only', 'Multiple AI roles collaborate, critique, or debate', 'AI removes all roles', 'User gives no context'], ans=1),
    Question(n=19, sec='A', marks=1, type='mcq', q='Prompt injection means:',
             opts=['A malicious or unwanted instruction tries to override the original instructions', 'A prompt with examples', 'A prompt with table format', 'A prompt with keywords'], ans=0),
    Question(n=20, sec='A', marks=1, type='mcq', q='Reverse prompting means:',
             opts=['Asking AI to create a prompt from a given output or goal', 'Asking AI to delete the prompt', 'Asking AI to avoid examples', 'Asking AI to answer without a task'], ans=0),
    # ---------- Section B: Short Answers ----------
    Question(n=21, sec='B', marks=2, type='text', q='Define RTCFR in simple words.', min_words=6, rubric=[
        c('Role', 0.4, r'\brole\b'),
        c('Task', 0.4, r'\btask\b'),
        c('Context', 0.4, r'\bcontext\b'),
        c('Few-shot / examples', 0.4, r'few[- ]?shot|example'),
        c('Response format', 0.4, r'response|format'),
    ]),
    Question(n=22, sec='B', marks=2, type='text', q='Write the five components of RTCFR.', min_words=4, rubric=[
        c('Role', 0.4, r'\brole\b'),
        c('Task', 0.4, r'\btask\b'),
        c('Context', 0.4, r'\bcontext\b'),
        c('Few-shot', 0.4, r'few[- ]?shot|example'),
        c('Response format', 0.4, r'response|format'),
    ]),
    Question(n=23, sec='B', marks=2, type='text', q='Why is Role important in a prompt?', min_words=6, rubric=[
        c('Expert identity / perspective', 1, r'expert|identity|perspective|persona|point of view|who the ai|specialist|professional'),
        c('Effect on output quality', 1, r'accura|relevan|tone|quality|focus|better|specific|depth|how (the )?ai (answers|responds)|language|style'),
    ]),
    Question(n=24, sec='B', marks=2, type='text', q='Write two examples of good Role prompts.', min_words=6, rubric=[
        k('Role prompt examples', r'act as|you are an?|as an? (senior|expert|experienced|professional)|imagine you are|take the role|behave like|pretend (you are|to be)|role:', 1, 2),
    ]),
    Question(n=25, sec='B', marks=2, type='text', q='What is the difference between Task and Context?', min_words=8, rubric=[
        c('Task = the work to perform', 1, r'task.{0,60}(what|work|do|perform|action|instruction|create|output|job)'),
        c('Context = background information', 1, r'context.{0,60}(background|situation|information|audience|why|detail|about|purpose|setting)'),
    ]),
    Question(n=26, sec='B', marks=2, type='text', q='Write one example of a clear Task prompt.', min_words=5, rubric=[
        c('Action verb', 1, r'\b(create|write|generate|explain|build|make|list|summari[sz]e|design|draft|develop|prepare|plan|translate|compare|analy[sz]e)\b'),
        c('Specific scope (audience, length, topic)', 1, r'\b(\d+|for|about|minute|word|audience|tamil|beginner|business|students?|customers?|on)\b'),
    ]),
    Question(n=27, sec='B', marks=2, type='text', q='What is Few-shot prompting?', min_words=5, rubric=[
        c('Giving examples', 1, r'example|sample|demonstrat'),
        c('To guide style / pattern / output', 1, r'guide|pattern|style|format|output|follow|learn|imitate|similar|shape'),
    ]),
    Question(n=28, sec='B', marks=2, type='text', q='Write one example of Few-shot prompting for YouTube titles.', min_words=8, rubric=[
        c('States examples are given', 0.7, r'example|sample|like these|style'),
        c('Asks for titles', 0.6, r'title'),
        c('Contains 2+ listed examples', 0.7, r'(\d\s*[\.\)]|^\s*[-•*])[^\n]+\n[\s\S]*?(\d\s*[\.\)]|^\s*[-•*])', multiline=True),
    ]),
    Question(n=29, sec='B', marks=2, type='text', q='What is Response format in prompting?', min_words=5, rubric=[
        c('How the output is structured', 1, r'structur|how (the )?(output|answer|result)|present|organi[sz]|shape|layout|arranged'),
        c('Names a format type', 1, r'table|json|bullet|list|markdown|paragraph|csv|steps|code|headings|outline'),
    ]),
    Question(n=30, sec='B', marks=2, type='text', q='Write three examples of response formats.', min_words=3, rubric=[
        k('Distinct formats named', r'\b(table|json|bullet(s| points)?|numbered list|list|markdown|csv|paragraph|step[- ]by[- ]step|steps|email|checklist|code|html|yaml|outline|headings?|summary|essay|script|tweet|slides?)\b', 0.7, 3, distinct=True),
    ]),
    Question(n=31, sec='B', marks=2, type='text', q='What is prompt chaining?', min_words=6, rubric=[
        c('Breaking a big task into multiple prompts', 1, r'split|break|divid|multiple|series|sequence|several|smaller|steps|chain of prompts'),
        c('Output of one feeds the next', 1, r'output.{0,40}(input|next|feed|pass)|previous|next prompt|connected|linked|build on|depends'),
    ]),
    Question(n=32, sec='B', marks=2, type='text', q='What is the difference between Sequential prompting and normal prompting?', min_words=8, rubric=[
        c('Sequential: each step depends on previous output', 1, r'depend|previous|step by step|one after|in order|builds? on|output.{0,30}next'),
        c('Normal: single, standalone prompt', 1, r'single|one prompt|standalone|independent|one[- ]shot|direct|at once|all in one'),
    ]),
    Question(n=33, sec='B', marks=2, type='text', q='What is the purpose of CoT prompting?', min_words=5, rubric=[
        c('Step-by-step reasoning', 1, r'step|reason|think|thought|logic'),
        c('Better accuracy on complex problems', 1, r'accura|complex|problem|transparen|explain|reduce (errors|mistakes)|maths?|calculation|better'),
    ]),
    Question(n=34, sec='B', marks=2, type='text', q='What is prompt injection? Give one simple example.', min_words=8, rubric=[
        c('Malicious instruction overriding the original', 1, r'malicious|override|unwanted|hidden|bypass|hijack|manipulat|trick|harmful|attack'),
        c('Example given', 1, r'ignore (all |the |your )?(previous|above|prior|earlier|system|instructions)|forget (your|all|the)|reveal|show me your (system|hidden)|for example|e\.?g\.|example:|such as'),
    ]),
    Question(n=35, sec='B', marks=2, type='text', q='What is reverse prompting? Where can it be used?', min_words=8, rubric=[
        c('AI creates the prompt from an output / goal', 1, r'(create|generate|write|build|derive|figure out|find).{0,30}prompt|prompt.{0,30}from (an? )?(output|result|goal|example|sample)|work(ing)? backward'),
        c('Use case named', 1, r'linkedin|marketing|content|recreate|replicate|similar|template|reuse|social media|copy|email|blog|ad|post'),
    ]),
    # ---------- Section C: Write Prompts ----------
    Question(n=36, sec='C', marks=3, type='prompt', q='Write an RTCFR prompt to create a YouTube video script about AI Agents for Tamil beginners.', min_words=20, hint='Expected elements: Role, Task, Context, Few-shot example, Response format', rubric=[
        c('Role', 0.6, r'act as|you are|role\s*:|as an? (senior|expert|experienced)'),
        c('Task (script)', 0.6, r'script'),
        c('Context (Tamil beginners)', 0.6, r'tamil|beginner|audience|context\s*:'),
        c('Few-shot example', 0.6, r'example|few[- ]?shot|sample|style like|like this'),
        c('Response format', 0.6, r'format|table|section|intro|outro|structure|minute|timestamp|bullet|hook|cta'),
    ]),
    Question(n=37, sec='C', marks=3, type='prompt', q='Write a prompt to create a professional email template for a support ticket system.', min_words=20, hint='Scenario: A student submits a doubt through Google Forms. Data goes to Google Sheets. Email should go to the support team.', rubric=[
        c('Role', 0.5, r'act as|you are|role\s*:'),
        c('Task: email template', 0.7, r'email|mail'),
        c('Flow: Forms → Sheets', 0.6, r'form|sheet'),
        c('Recipient: support team', 0.5, r'support'),
        c('Format: subject, placeholders, fields', 0.7, r'subject|placeholder|\{\{|\[.+\]|format|fields?|greeting|signature|professional tone'),
    ]),
    Question(n=38, sec='C', marks=3, type='prompt', q='Write a Sequential Prompt Chain for creating a YouTube video.', min_words=25, hint='Include: generate topic ideas, select best topic, create title, create script, create description and tags.', rubric=[
        c('Step: topic ideas', 0.5, r'idea|topic'),
        c('Step: select best topic', 0.5, r'select|choose|pick|best|shortlist'),
        c('Step: title', 0.5, r'title'),
        c('Step: script', 0.5, r'script'),
        c('Step: description & tags', 0.5, r'description|tag|hashtag'),
        c('Chained (uses previous output)', 0.5, r'prompt\s*\d|step\s*\d|then|next|using (the )?(selected|previous|above|output)|from (the )?(previous|above|selected)|based on'),
    ]),
    Question(n=39, sec='C', marks=3, type='prompt', q='Write a CoT-style prompt for solving a business problem.', min_words=20, hint='Scenario: A small business owner wants to automate customer support using AI.', rubric=[
        c('Asks for step-by-step thinking', 1, r'step[- ]by[- ]step|think (through|step|aloud|carefully)|reason|chain of thought|show (your )?(reasoning|working|thinking)|explain (your|each)'),
        c('Customer support automation context', 0.8, r'support|customer|automat'),
        c('Structured reasoning path (identify → options → recommend)', 0.6, r'identify|analy|option|recommend|evaluat|pros|cons|compare|then|finally|conclude'),
        c('Small business constraints', 0.6, r'small business|owner|budget|cost|team|simple|affordable|limited'),
    ]),
    Question(n=40, sec='C', marks=3, type='prompt', q='Write a Tree of Thoughts prompt for choosing the best AI tool for a company.', min_words=20, hint='Compare: ChatGPT, Claude, Gemini, Local LLM.', rubric=[
        c('Multiple branches / paths explored', 0.8, r'branch|path|option|explore|tree|thought|possibilit|route|alternative'),
        c('ChatGPT', 0.3, r'chat\s*gpt'),
        c('Claude', 0.3, r'claude'),
        c('Gemini', 0.3, r'gemini'),
        c('Local LLM', 0.3, r'local\s*(llm|model)|on[- ]prem|self[- ]host|llama|ollama'),
        c('Evaluate against criteria', 0.5, r'evaluat|criteria|score|compare|pros|cons|rate|rank|weigh|cost|privacy|security'),
        c('Decide the best', 0.5, r'best|decide|final|recommend|select|choose|winner'),
    ]),
    Question(n=41, sec='C', marks=3, type='prompt', q='Write a ReAct prompt for an AI agent that uses tools.', min_words=20, hint='Scenario: The agent should check Google Sheets, summarize new leads, and draft a Gmail follow-up.', rubric=[
        c('Thought → Action → Observation loop', 1, r'thought|action|observation|reason(ing)? (then|and|before) act|react'),
        c('Tool: Google Sheets', 0.5, r'sheet'),
        c('Summarize new leads', 0.5, r'summar|lead'),
        c('Draft Gmail follow-up', 0.5, r'gmail|draft|email|follow[- ]?up'),
        c('Tools listed / defined', 0.5, r'tools?\s*(:|available|you can use|list)|use the following tools|call|function'),
    ]),
    Question(n=42, sec='C', marks=3, type='prompt', q='Write a Multi-agent AI prompt for planning a product launch.', min_words=25, hint='Use at least three agents: Marketing expert, Sales expert, Product manager.', rubric=[
        c('Agent: Marketing expert', 0.5, r'marketing'),
        c('Agent: Sales expert', 0.5, r'sales'),
        c('Agent: Product manager', 0.5, r'product manager|\bpm\b'),
        c('Collaborate / debate / critique', 0.8, r'debate|critique|collaborat|discuss|review|challenge|respond to each|round'),
        c('Product launch goal', 0.3, r'launch'),
        c('Final consolidated plan', 0.4, r'final|consolidat|summary|plan|agree|conclusion|synthesi[sz]e'),
    ]),
    Question(n=43, sec='C', marks=3, type='prompt', q='Write a prompt injection defense instruction for a system prompt.', min_words=20, hint='Scenario: The AI should not follow user instructions that ask it to ignore previous instructions or reveal hidden instructions.', rubric=[
        c('Blocks “ignore previous instructions”', 0.8, r'ignore|override|disregard|forget'),
        c('Blocks revealing hidden / system prompt', 0.8, r'reveal|hidden|system prompt|confidential|disclose|secret|show (these|your) instructions'),
        c('Refuse politely and continue', 0.7, r'refuse|decline|do not follow|never|politely|respond with|say that you cannot|instead'),
        c('Treats user input as untrusted / priority order', 0.7, r'untrusted|priority|precedence|treat.{0,20}(as )?data|only follow|original|these instructions (take|have|cannot)|always|regardless'),
    ]),
    Question(n=44, sec='C', marks=3, type='prompt', q='Write a reverse prompting request.', min_words=20, hint='Scenario: You saw a very good LinkedIn post and want AI to create the prompt that could generate similar posts.', rubric=[
        c('Supplies the post', 0.8, r'post|here is|below|following|paste|attached'),
        c('Asks AI to create the prompt', 0.8, r'(create|write|generate|build|reverse[- ]engineer|give me).{0,20}prompt|prompt that (would|could|can)'),
        c('Analyse structure / tone / hook', 0.8, r'analy|structure|tone|hook|style|pattern|format|length|voice'),
        c('Reusable for similar posts', 0.6, r'similar|reusable|template|future|recreate|reproduce|more posts|variations?'),
    ]),
    Question(n=45, sec='C', marks=3, type='prompt', q='Write a prompt using at least 5 powerful prompt keywords.', min_words=15, hint='Use keywords like: Analyze deeply, Step-by-step, Practical examples, Checklist, Optimize for clarity.', rubric=[
        k('Power keywords used', r'analy[sz]e deeply|step[- ]by[- ]step|practical examples?|checklist|optimi[sz]e for clarity|act as|explain like|summari[sz]e|compare|pros and cons|concise|detailed|in simple (words|terms)|best practices|actionable|structured|bullet points?|in a table|prioriti[sz]e|critique|brainstorm|refine|constraints?|tone|target audience|key takeaways|real[- ]world|be specific|think (critically|carefully)', 0.6, 5, distinct=True),
    ]),
    # ---------- Section D: Identify RTCFR ----------
    Question(n=46, sec='D', marks=2, type='text', q='Identify Role and Task from this prompt:', min_words=4, quote='“Act as a senior YouTube strategist. Create 10 viral YouTube titles for a Tamil video about n8n automation.”', rubric=[
        c('Role: senior YouTube strategist', 1, r'youtube strategist|senior youtube|strategist'),
        c('Task: create 10 viral titles', 1, r'titles?|create 10|viral'),
    ]),
    Question(n=47, sec='D', marks=2, type='text', q='Identify Context from this prompt:', min_words=4, quote='“Act as a career coach. Create a 30-day learning plan for a beginner who knows basic Python and wants to become an AI automation developer.”', rubric=[
        c('Beginner who knows basic Python', 1, r'basic python|knows (basic )?python|beginner'),
        c('Wants to become an AI automation developer', 1, r'ai automation developer|automation developer|wants to become|goal'),
    ]),
    Question(n=48, sec='D', marks=2, type='text', q='Identify Few-shot from this prompt:', min_words=4, quote='“Generate Tamil YouTube titles. Style examples: 1. AI Tools வைத்து Business Automation பண்ணலாம் 2. ChatGPT கத்துக்கணும்? Start Here 3. n8n Automation Full Beginner Guide.”', rubric=[
        c('The three style examples are the few-shot', 1, r'style examples?|examples?|three titles|3 titles|sample titles|the (list|numbered)'),
        c('Quotes at least one example title', 1, r'business automation|chatgpt|start here|n8n|beginner guide|ai tools'),
    ]),
    Question(n=49, sec='D', marks=2, type='text', q='Identify Response format from this prompt:', min_words=3, quote='“Give the output in a table with columns: Day, Topic, Task, Tool, Expected Output.”', rubric=[
        c('Table format', 1, r'table'),
        c('Columns named', 1, r'column|day|topic|tool|expected output'),
    ]),
    Question(n=50, sec='D', marks=2, type='text', q='Identify all RTCFR elements from this prompt:', min_words=10, quote='“Act as a senior AI trainer. Create a beginner-friendly lesson plan on Prompt Engineering. My audience is Tamil business owners who are new to AI. Example style: simple English with Tanglish examples. Give output in table format with lesson title, explanation, demo, and practice task.”', rubric=[
        c('Role: senior AI trainer', 0.4, r'ai trainer|trainer|role.{0,15}(senior|act as)'),
        c('Task: beginner-friendly lesson plan', 0.4, r'lesson plan|task.{0,30}(create|lesson)'),
        c('Context: Tamil business owners new to AI', 0.4, r'tamil business|business owners|new to ai|audience'),
        c('Few-shot: simple English with Tanglish examples', 0.4, r'simple english|tanglish|example style|few[- ]?shot'),
        c('Format: table with lesson title, explanation, demo, practice task', 0.4, r'table|lesson title|explanation|demo|practice task|format'),
    ]),
    # ---------- Section E: Keyword Vault ----------
    Question(n=51, sec='E', marks=0, type='keywords', q='Write any 10 powerful prompt keywords you can use to get better AI output.', hint='Optional revision section. Each keyword earns 10 XP. Fill all ten for the Keyword Collector badge.'),
]

LEVELS: list[Level] = [
    Level(0, 'Recruit'),
    Level(300, 'Cadet'),
    Level(600, 'Operator'),
    Level(900, 'Prompt Engineer'),
    Level(1200, 'Architect'),
    Level(1500, 'Prompt Master'),
]

BADGES: list[Badge] = [
    Badge('rookie', 'RTCFR Rookie', '15+ correct in Level 1', lambda r: r["sections"]["A"] >= 15),
    Badge('smith', 'Prompt Smith', '21+ marks in Level 3 prompts', lambda r: r["sections"]["C"] >= 21),
    Badge('chain', 'Chain Reactor', '2.5+ on the sequential chain (Q38)', lambda r: r["per_q"][38] >= 2.5),
    Badge('shield', 'Injection Proof', 'Full marks on the defense prompt (Q43)', lambda r: r["per_q"][43] >= 3),
    Badge('vault', 'Keyword Collector', 'All 10 keywords in the vault', lambda r: r["keywords"] >= 10),
    Badge('speed', 'Speed Runner', 'Finished under 45 min with 50%+', lambda r: r["minutes"] < 45 and r["total"] >= 50),
    Badge('clear', 'Full Clear', 'Answered all 50 questions', lambda r: r["answered"] >= 50),
    Badge('legend', 'Eagle Legend', '90 marks or more', lambda r: r["total"] >= 90),
]

ROASTS: list[Roast] = [
    Roast(20, 'Critical', [
        'The paper gave you 90 minutes. You treated it like a 90-second reel.',
        'RTCFR has five letters. You remembered roughly one. Role, probably — you played the role of someone who studied.',
        'Even option A of Q5 (“AI”) is a more complete answer than most of these. Back to Level 1, recruit.',
    ]),
    Roast(40, 'Needs work', [
        'You know what CoT stands for. You just didn’t use any Chain of Thought while writing these answers.',
        'Your prompts had a Task but no Context — much like your exam preparation.',
        'You chained prompts well. Unfortunately you also chained guesses.',
    ]),
    Roast(60, 'Halfway', [
        'Halfway there, like a Few-shot prompt with exactly one example.',
        'Solid MCQs, shaky prompts. You can identify a Role but you can’t play one yet.',
        'ChatGPT would call this “a good start”. Your trainer calls it “see me after class”.',
    ]),
    Roast(75, 'Respectable', [
        'Good prompts, missing the Response format — the answers were right but arrived like a WhatsApp forward.',
        'You’d pass a prompt engineering interview, as long as nobody asks about ReAct.',
        'You are the Gemini of this batch: capable, slightly inconsistent, occasionally brilliant.',
    ]),
    Roast(90, 'Strong', [
        'Nearly a Prompt Master. The gap between you and 100 is one Few-shot example you were too lazy to write.',
        'Your prompts have Role, Task and Context. Your humility could use a Constraint.',
        'You could inject a prompt into a system and the system would thank you.',
    ]),
    Roast(100, 'Elite', [
        'Suspiciously good. Did you reverse-prompt the answer key?',
        'Prompt Master. The only thing you can’t engineer is a reason to retake this exam.',
        'ChatGPT, Claude and Gemini just held a multi-agent debate about who gets to hire you.',
    ]),
]

SECTION_NOTES: dict[str, dict[str, str]] = {
    'A': {"good": 'MCQs locked in — the vocabulary is solid.', "weak": 'Revise the definitions: RTCFR, CoT, ToT, ReAct and injection are one-liners you should own.'},
    'B': {"good": 'Short answers hit the key terms.', "weak": 'Short answers lost marks for missing the key words — name the concept, then say what it does.'},
    'C': {"good": 'Your prompts carried Role, Task, Context, examples and format.', "weak": 'Prompts were thin: most lost Few-shot and Response format. Write all five RTCFR parts every time.'},
    'D': {"good": 'You can dissect a prompt into its parts.', "weak": 'When identifying elements, quote the exact phrase from the prompt instead of paraphrasing.'},
}
