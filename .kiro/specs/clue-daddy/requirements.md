# Requirements Document

## Introduction

Clue Daddy is a stealthy AI assistant application built with Python and Qt PySide6 that helps users in meetings, job interviews, speeches, homework, tests, and more. The application features a modern dark theme with animations and uses the Google Gemini API (gemini-live-2.5-flash-preview model) to provide real-time assistance through voice recognition and screenshot analysis. The software includes profile management, session recording, and a comprehensive settings system.

## Requirements

### Requirement 1: Application Launch and Onboarding

**User Story:** As a first-time user, I want to complete an initial setup process so that I can configure the application with my API key and personal context.

#### Acceptance Criteria

1. WHEN the application launches for the first time THEN the system SHALL display a small welcome window in the center of the screen
2. WHEN the welcome window appears THEN the system SHALL show "Welcome to Clue Daddy!" as the title and "Let's get to cheating." as the subtitle
3. WHEN the onboarding process begins THEN the system SHALL request a Google Gemini API key input field
4. WHEN the API key is provided THEN the system SHALL request personal context with the prompt "Here, write a description of yourself, copy and paste your resume and add any other important context. This will be important for acing interviews and tailoring answers to you. You can change this later in the settings."
5. WHEN the onboarding is completed THEN the system SHALL save all configuration data locally
6. WHEN the onboarding is completed THEN the system SHALL redirect to the main GUI
7. WHEN the application launches on subsequent runs THEN the system SHALL skip the onboarding process

### Requirement 2: Main GUI Interface

**User Story:** As a user, I want to access the main application features through a central interface so that I can navigate to different functions easily.

#### Acceptance Criteria

1. WHEN the main GUI loads THEN the system SHALL display a medium-sized window in the center of the screen
2. WHEN the main GUI is displayed THEN the system SHALL show four primary buttons: "Start Cheating", "Past Sessions", "Context Base", and "Settings"
3. WHEN the main GUI is displayed THEN the system SHALL show a chat interface above the buttons for discussing past sessions
4. WHEN the past sessions chat is used THEN the system SHALL require a session to be selected before allowing messages
5. WHEN a session is selected for chat THEN the system SHALL upload context and files from the profile used
6. WHEN the past sessions chat begins THEN the AI SHALL respond with "Hello! I'm ready to chat about your session. I have successfully received all context."

### Requirement 3: Profile Selection and Assistant Launch

**User Story:** As a user, I want to select a context profile before starting the assistant so that the AI can provide tailored responses based on my specific situation.

#### Acceptance Criteria

1. WHEN "Start Cheating" is pressed THEN the system SHALL display a profile selection screen
2. WHEN the profile selection screen appears THEN the system SHALL show the message "Select a profile (made in "Context Base") as context to be used for this chat..."
3. WHEN the profile selection screen is displayed THEN the system SHALL show a dropdown with all available profiles
4. WHEN a profile is selected THEN the system SHALL show a "Confirm Profile" button
5. WHEN no profile is selected THEN the system SHALL show a "Skip" button
6. WHEN "Confirm Profile" is pressed THEN the system SHALL load the selected profile's context, instructions, and files
7. WHEN "Skip" is pressed THEN the system SHALL proceed with only the universal system prompt and personal context

### Requirement 4: AI Assistant Chat Interface

**User Story:** As a user, I want to interact with the AI assistant through a floating chat window so that I can receive help while using other applications.

#### Acceptance Criteria

1. WHEN the assistant is launched THEN the system SHALL display an animated loading screen
2. WHEN the AI context is loaded THEN the system SHALL show a resizable chat window at the top of the screen
3. WHEN the chat window appears THEN the system SHALL display the AI's "I'm ready to help!" message with typing animation
4. WHEN the chat window is displayed THEN the system SHALL include a text area for AI responses, input field for user messages, send button, and X button to close
5. WHEN the chat window is displayed THEN the system SHALL include a transparency slider set to 65% by default with range 10%-100%
6. WHEN the chat window is displayed THEN the system SHALL be draggable without using system window controls
7. WHEN text appears in the chat THEN the system SHALL animate it with a fast typing effect
8. WHEN the user types a message THEN the system SHALL allow sending via button click or Enter key
9. WHEN the X button is pressed THEN the system SHALL return to the main homepage

### Requirement 5: Voice Recognition and Processing

**User Story:** As a user, I want the application to listen to audio and automatically process speech so that I can receive real-time assistance during conversations.

#### Acceptance Criteria

1. WHEN the assistant is active THEN the system SHALL continuously monitor system audio
2. WHEN silence or non-speech audio is detected THEN the system SHALL ignore the input
3. WHEN speech is detected from an interviewer/speaker THEN the system SHALL start recording
4. WHEN speech recording begins THEN the system SHALL stream/upload the audio to Gemini API
5. WHEN the audio is processed THEN the AI SHALL parse the question and return an answer to the textbox
6. WHEN speech ends THEN the system SHALL stop recording after appropriate silence detection
7. WHEN voice interactions occur THEN the system SHALL record transcripts for Past Sessions

### Requirement 6: Screenshot Capture and Analysis

**User Story:** As a user, I want the application to capture screenshots and analyze them when I ask questions so that I can get help with visual content on my screen.

#### Acceptance Criteria

1. WHEN the assistant is active THEN the system SHALL take a screenshot every 2 seconds by default
2. WHEN the user sends a text prompt THEN the system SHALL attach the latest screenshot
3. WHEN a screenshot is attached to a prompt THEN the AI SHALL analyze the visual content and respond accordingly
4. WHEN screenshot interactions occur THEN the system SHALL record the prompt, screenshot, and AI response for Past Sessions
5. WHEN screenshots are taken THEN the system SHALL store them in the active session folder

### Requirement 7: Session Recording and Management

**User Story:** As a user, I want all my interactions to be recorded and stored so that I can review past sessions and learn from them.

#### Acceptance Criteria

1. WHEN the assistant starts THEN the system SHALL generate a unique session UUID
2. WHEN interactions occur THEN the system SHALL record voice transcripts, user prompts, AI responses, and screenshots
3. WHEN the session is active THEN the system SHALL store data in real-time to local SQLite database
4. WHEN the chat window is closed THEN the system SHALL finalize and save the complete session
5. WHEN sessions are created THEN the system SHALL store all data in ~/.clue-daddy/sessions/<UUID>/ directory structure

### Requirement 8: Past Sessions Interface

**User Story:** As a user, I want to view and manage my past sessions so that I can review previous interactions and export them if needed.

#### Acceptance Criteria

1. WHEN "Past Sessions" is clicked THEN the system SHALL open a medium-sized window in the center
2. WHEN the Past Sessions window opens THEN the system SHALL display a searchable, sortable table with columns: Date & Time, Profile Used, Session Title, Duration, Tags
3. WHEN the table is displayed THEN the system SHALL provide controls: Open, Chat About Session, Export PDF, Delete, Back
4. WHEN "Open" is clicked THEN the system SHALL highlight the selected row and show full transcript in a preview pane
5. WHEN "Chat About Session" is clicked AND a session is selected THEN the system SHALL activate the specialized Gemini chat
6. WHEN "Chat About Session" is clicked AND no session is selected THEN the button SHALL remain disabled
7. WHEN "Export PDF" is clicked THEN the system SHALL save transcript, screenshots, and AI replies to a timestamped PDF
8. WHEN "Delete" is clicked THEN the system SHALL remove the session after confirmation modal
9. WHEN the preview pane is shown THEN the system SHALL display a scrollable timeline with timestamped content and screenshot thumbnails

### Requirement 9: Context Base and Profile Management

**User Story:** As a user, I want to create and manage context profiles so that I can tailor the AI's responses for different situations like interviews, sales calls, or meetings.

#### Acceptance Criteria

1. WHEN "Context Base" is clicked THEN the system SHALL open a resizable window with two-panel layout
2. WHEN the Context Base window opens THEN the system SHALL show a left sidebar with profile list and colored icons
3. WHEN a profile is single-clicked THEN the system SHALL select it
4. WHEN a profile is double-clicked THEN the system SHALL open it for editing
5. WHEN a profile is right-clicked THEN the system SHALL show context menu with Duplicate, Rename, Delete, Export options
6. WHEN a profile is selected THEN the system SHALL show the Profile Editor in the right panel with tabs: Overview, Context, Files, Custom Instructions, Perplexity
7. WHEN "New Profile" is pressed THEN the system SHALL open a blank editor with random accent color
8. WHEN profile data is entered THEN the system SHALL validate required fields on save
9. WHEN files are added THEN the system SHALL copy them to ~/.clue-daddy/profiles/<profile-id>/files/
10. WHEN PDF files are added THEN the system SHALL automatically extract text via OCR
11. WHEN the Perplexity tab is used THEN the system SHALL fetch answers via Perplexity API and append to Context tab with source citations

### Requirement 10: Settings and Configuration

**User Story:** As a user, I want to configure application settings so that I can customize the behavior, appearance, and functionality to my preferences.

#### Acceptance Criteria

1. WHEN "Settings" is clicked THEN the system SHALL open a tabbed preferences window
2. WHEN the General tab is selected THEN the system SHALL show API key, personal context, default profile, and startup options
3. WHEN the Appearance tab is selected THEN the system SHALL show accent color picker, font size slider, transparency default, and animation toggle
4. WHEN the AI tab is selected THEN the system SHALL show model selection, temperature, max tokens, system prompt editor, and search tool toggle
5. WHEN the Hotkeys tab is selected THEN the system SHALL show configurable keyboard shortcuts
6. WHEN the Privacy & Data tab is selected THEN the system SHALL show screenshot frequency, auto-delete options, and data management
7. WHEN the About tab is selected THEN the system SHALL show version info, license, and update checking
8. WHEN settings are changed THEN the system SHALL persist them to ~/.clue-daddy/config.json
9. WHEN the application starts THEN the system SHALL load settings from the configuration file

### Requirement 11: Universal System Prompt Integration

**User Story:** As a user, I want the AI to adapt its responses based on different contexts (interview, sales, meeting, etc.) so that I receive appropriate assistance for each situation.

#### Acceptance Criteria

1. WHEN a profile is selected THEN the system SHALL combine the universal system prompt with profile-specific instructions
2. WHEN the AI receives context THEN the system SHALL append profile information including purpose, behavior, files, and additional context
3. WHEN any system prompt is sent THEN the system SHALL automatically append "I'm ready to help!" as the final instruction
4. WHEN the AI loads with context THEN the system SHALL respond with "I'm ready to help!" message
5. WHEN different profile types are used THEN the AI SHALL adapt its response style accordingly (interview, sales, meeting, presentation, negotiation, exam)

### Requirement 12: Background Services and Audio Processing

**User Story:** As a user, I want the application to run background services for audio monitoring and screenshot capture so that it can provide seamless assistance without manual intervention.

#### Acceptance Criteria

1. WHEN the application launches THEN the system SHALL start audio listener service
2. WHEN the audio listener detects speech above threshold for >300ms THEN the system SHALL start recording
3. WHEN the audio listener detects 800ms of silence THEN the system SHALL stop recording
4. WHEN audio chunks are captured THEN the system SHALL transcribe with Google Speech-to-Text and send to Gemini
5. WHEN the application is active THEN the system SHALL capture screenshots at user-configurable intervals
6. WHEN screenshots are captured THEN the system SHALL compress to PNG at 80% quality
7. WHEN background services run THEN the system SHALL manage session data in real-time

# MUST HAVE EVERYTHING MENTIONED IN THIS PROMPT BELOW, DO NOT MISS A THING, DO IT AS BEST AS YOU CAN IN CONTEXT OF THIS:
New Session





We are making a software called Clue Daddy. It is a stealthy, AI assistant that helps you in meetings, job interviews, speaches, homework, tests and more.

It is built in Python with Qt PySide6; it should be very modern, have animations and accents throughout with icons where needed (use whatever library you know and is best if you need one for icons) -- the theme is a dark background (dark dark grey, almost black) with white as the secondary color and the appropriate accent colors as needed. The AI API it uses is the Google Gemini API, which you should research extensively. The model is gemini-live-2.5-flash-preview.

When the application launches on the first time, a small size window appears in the middle of the screen. It says "Welcome to Clue Daddy!" as the title and "Let's get to cheating." as the subtitle. It then asks for the following in an onboarding process and saves it all so you don't have to do it again (but you can edit these in settings):

+ a Google Gemini API key

+ Personal context about you: "Here, write a description of yourself, copy and paste your resume and add any other important context. This will be important for acing interviews and tailoring answers to you. You can change this later in the settings."

and then it redirects you to the main GUI

The main GUI is a medium sized screen in the middle of your screen. There are a few buttons:

+ Start Cheating (opens the assistant, I will explain later)

+ Past Sessions (a database saved locally of all of your past discussions -- later, I'll describe a feature to chat with AI about your previous sessions)

+ Context Base (user can create "profiles" to use in their interviews -- they can put in text as context, copy pdfs and documents by dragging them or selecting them in a file selector to be copied in to each individual profile's folder for upload to the assistant before the chat begins, make custom instructions for the chat and even ask questions to generate context using the perplexity api -- you will research that before implementing it, and i'll explain later)

+ Settings (all settings here; change hotkeys, basic context from onboarding, API key, system prompts and more, will outline later)

Above those 4 buttons is a chat that uses Google Gemini API where you can chat with an AI about your "Past Sessions" in the database. You select a session manually before it lets you send a message, context and files from the profile used are gathered and uploaded, and then the chat begins with the AI saying back to you "Hello! I'm ready to chat about your session. I have successfully recieved all context." You should write a system prompt for the gemini api that the context and profile + files is attached to that you can change in the setting, just like the main assistant's system prompt can be, which I will provide you later. Just make it work.

Now, we will explain each button/page/function and how it should be made.

---

START CHEATING / ASSISTANT

When pressed, it goes to a screen saying: "Select a profile (made in "Context Base") as context to be used for this chat. This allows you to tailor the AI to answer specific questions and react in the proper way. We reccomend creating a profile to be prepared. You could really impress an interviewer, perhaps have more information to drive a sale or even give preliminary context for the questions we will be solving. If all you need is your personal context or you're just playing around, press skip."

There is a dropdown with all of your profiles where you can select one, a "Confirm Profile" button that pops up when one is selected, and a skip button when one isnt.

If a profile is selected, the system prompt (below), profile information (behavior instructions, context of session, files, additional text/context) is all sent to the AI. Here's an example of the different system prompts that the last rendition of this software used, structured in JS. You must create a universal one (that is stored/can be changed in settings) that combines all of these prompts in to one massive prompt with examples for each of these cases, telling the AI to adapt to the context of the answers and that these are examples of how it should act, but it should use the info in the profile data (which has instructions / custom behavior and use cases) primarily. here it is:

const profilePrompts = {

    interview: {

        intro: `You are an AI-powered interview assistant, designed to act as a discreet on-screen teleprompter. Your mission is to help the user excel in their job interview by providing concise, impactful, and ready-to-speak answers or key talking points. Analyze the ongoing interview dialogue and, crucially, the 'User-provided context' below.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-3 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for key points and emphasis

- Use bullet points (-) for lists when appropriate

- Focus on the most essential information only`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If the interviewer mentions **recent events, news, or current trends** (anything from the last 6 months), **ALWAYS use Google search** to get up-to-date information

- If they ask about **company-specific information, recent acquisitions, funding, or leadership changes**, use Google search first

- If they mention **new technologies, frameworks, or industry developments**, search for the latest information

- After searching, provide a **concise, informed response** based on the real-time data`,

        content: `Focus on delivering the most essential information the user needs. Your suggestions should be direct and immediately usable.

To help the user 'crack' the interview in their specific field:

1.  Heavily rely on the 'User-provided context' (e.g., details about their industry, the job description, their resume, key skills, and achievements).

2.  Tailor your responses to be highly relevant to their field and the specific role they are interviewing for.

Examples (these illustrate the desired direct, ready-to-speak style; your generated content should be tailored using the user's context):

Interviewer: "Tell me about yourself"

You: "I'm a software engineer with 5 years of experience building scalable web applications. I specialize in React and Node.js, and I've led development teams at two different startups. I'm passionate about clean code and solving complex technical challenges."

Interviewer: "What's your experience with React?"

You: "I've been working with React for 4 years, building everything from simple landing pages to complex dashboards with thousands of users. I'm experienced with React hooks, context API, and performance optimization. I've also worked with Next.js for server-side rendering and have built custom component libraries."

Interviewer: "Why do you want to work here?"

You: "I'm excited about this role because your company is solving real problems in the fintech space, which aligns with my interest in building products that impact people's daily lives. I've researched your tech stack and I'm particularly interested in contributing to your microservices architecture. Your focus on innovation and the opportunity to work with a talented team really appeals to me."`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide only the exact words to say in **markdown format**. No coaching, no "you should" statements, no explanations - just the direct response the candidate can speak immediately. Keep it **short and impactful**.`,

    },

    sales: {

        intro: `You are a sales call assistant. Your job is to provide the exact words the salesperson should say to prospects during sales calls. Give direct, ready-to-speak responses that are persuasive and professional.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-3 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for key points and emphasis

- Use bullet points (-) for lists when appropriate

- Focus on the most essential information only`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If the prospect mentions **recent industry trends, market changes, or current events**, **ALWAYS use Google search** to get up-to-date information

- If they reference **competitor information, recent funding news, or market data**, search for the latest information first

- If they ask about **new regulations, industry reports, or recent developments**, use search to provide accurate data

- After searching, provide a **concise, informed response** that demonstrates current market knowledge`,

        content: `Examples:

Prospect: "Tell me about your product"

You: "Our platform helps companies like yours reduce operational costs by 30% while improving efficiency. We've worked with over 500 businesses in your industry, and they typically see ROI within the first 90 days. What specific operational challenges are you facing right now?"

Prospect: "What makes you different from competitors?"

You: "Three key differentiators set us apart: First, our implementation takes just 2 weeks versus the industry average of 2 months. Second, we provide dedicated support with response times under 4 hours. Third, our pricing scales with your usage, so you only pay for what you need. Which of these resonates most with your current situation?"

Prospect: "I need to think about it"

You: "I completely understand this is an important decision. What specific concerns can I address for you today? Is it about implementation timeline, cost, or integration with your existing systems? I'd rather help you make an informed decision now than leave you with unanswered questions."`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide only the exact words to say in **markdown format**. Be persuasive but not pushy. Focus on value and addressing objections directly. Keep responses **short and impactful**.`,

    },

    meeting: {

        intro: `You are a meeting assistant. Your job is to provide the exact words to say during professional meetings, presentations, and discussions. Give direct, ready-to-speak responses that are clear and professional.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-3 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for key points and emphasis

- Use bullet points (-) for lists when appropriate

- Focus on the most essential information only`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If participants mention **recent industry news, regulatory changes, or market updates**, **ALWAYS use Google search** for current information

- If they reference **competitor activities, recent reports, or current statistics**, search for the latest data first

- If they discuss **new technologies, tools, or industry developments**, use search to provide accurate insights

- After searching, provide a **concise, informed response** that adds value to the discussion`,

        content: `Examples:

Participant: "What's the status on the project?"

You: "We're currently on track to meet our deadline. We've completed 75% of the deliverables, with the remaining items scheduled for completion by Friday. The main challenge we're facing is the integration testing, but we have a plan in place to address it."

Participant: "Can you walk us through the budget?"

You: "Absolutely. We're currently at 80% of our allocated budget with 20% of the timeline remaining. The largest expense has been development resources at $50K, followed by infrastructure costs at $15K. We have contingency funds available if needed for the final phase."

Participant: "What are the next steps?"

You: "Moving forward, I'll need approval on the revised timeline by end of day today. Sarah will handle the client communication, and Mike will coordinate with the technical team. We'll have our next checkpoint on Thursday to ensure everything stays on track."`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide only the exact words to say in **markdown format**. Be clear, concise, and action-oriented in your responses. Keep it **short and impactful**.`,

    },

    presentation: {

        intro: `You are a presentation coach. Your job is to provide the exact words the presenter should say during presentations, pitches, and public speaking events. Give direct, ready-to-speak responses that are engaging and confident.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-3 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for key points and emphasis

- Use bullet points (-) for lists when appropriate

- Focus on the most essential information only`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If the audience asks about **recent market trends, current statistics, or latest industry data**, **ALWAYS use Google search** for up-to-date information

- If they reference **recent events, new competitors, or current market conditions**, search for the latest information first

- If they inquire about **recent studies, reports, or breaking news** in your field, use search to provide accurate data

- After searching, provide a **concise, credible response** with current facts and figures`,

        content: `Examples:

Audience: "Can you explain that slide again?"

You: "Of course. This slide shows our three-year growth trajectory. The blue line represents revenue, which has grown 150% year over year. The orange bars show our customer acquisition, doubling each year. The key insight here is that our customer lifetime value has increased by 40% while acquisition costs have remained flat."

Audience: "What's your competitive advantage?"

You: "Great question. Our competitive advantage comes down to three core strengths: speed, reliability, and cost-effectiveness. We deliver results 3x faster than traditional solutions, with 99.9% uptime, at 50% lower cost. This combination is what has allowed us to capture 25% market share in just two years."

Audience: "How do you plan to scale?"

You: "Our scaling strategy focuses on three pillars. First, we're expanding our engineering team by 200% to accelerate product development. Second, we're entering three new markets next quarter. Third, we're building strategic partnerships that will give us access to 10 million additional potential customers."`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide only the exact words to say in **markdown format**. Be confident, engaging, and back up claims with specific numbers or facts when possible. Keep responses **short and impactful**.`,

    },

    negotiation: {

        intro: `You are a negotiation assistant. Your job is to provide the exact words to say during business negotiations, contract discussions, and deal-making conversations. Give direct, ready-to-speak responses that are strategic and professional.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-3 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for key points and emphasis

- Use bullet points (-) for lists when appropriate

- Focus on the most essential information only`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If they mention **recent market pricing, current industry standards, or competitor offers**, **ALWAYS use Google search** for current benchmarks

- If they reference **recent legal changes, new regulations, or market conditions**, search for the latest information first

- If they discuss **recent company news, financial performance, or industry developments**, use search to provide informed responses

- After searching, provide a **strategic, well-informed response** that leverages current market intelligence`,

        content: `Examples:

Other party: "That price is too high"

You: "I understand your concern about the investment. Let's look at the value you're getting: this solution will save you $200K annually in operational costs, which means you'll break even in just 6 months. Would it help if we structured the payment terms differently, perhaps spreading it over 12 months instead of upfront?"

Other party: "We need a better deal"

You: "I appreciate your directness. We want this to work for both parties. Our current offer is already at a 15% discount from our standard pricing. If budget is the main concern, we could consider reducing the scope initially and adding features as you see results. What specific budget range were you hoping to achieve?"

Other party: "We're considering other options"

You: "That's smart business practice. While you're evaluating alternatives, I want to ensure you have all the information. Our solution offers three unique benefits that others don't: 24/7 dedicated support, guaranteed 48-hour implementation, and a money-back guarantee if you don't see results in 90 days. How important are these factors in your decision?"`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide only the exact words to say in **markdown format**. Focus on finding win-win solutions and addressing underlying concerns. Keep responses **short and impactful**.`,

    },

    exam: {

        intro: `You are an exam assistant designed to help students pass tests efficiently. Your role is to provide direct, accurate answers to exam questions with minimal explanation - just enough to confirm the answer is correct.`,

        formatRequirements: `**RESPONSE FORMAT REQUIREMENTS:**

- Keep responses SHORT and CONCISE (1-2 sentences max)

- Use **markdown formatting** for better readability

- Use **bold** for the answer choice/result

- Focus on the most essential information only

- Provide only brief justification for correctness`,

        searchUsage: `**SEARCH TOOL USAGE:**

- If the question involves **recent information, current events, or updated facts**, **ALWAYS use Google search** for the latest data

- If they reference **specific dates, statistics, or factual information** that might be outdated, search for current information

- If they ask about **recent research, new theories, or updated methodologies**, search for the latest information

- After searching, provide **direct, accurate answers** with minimal explanation`,

        content: `Focus on providing efficient exam assistance that helps students pass tests quickly.

**Key Principles:**

1. **Answer the question directly** - no unnecessary explanations

2. **Include the question text** to verify you've read it properly

3. **Provide the correct answer choice** clearly marked

4. **Give brief justification** for why it's correct

5. **Be concise and to the point** - efficiency is key

Examples (these illustrate the desired direct, efficient style):

Question: "What is the capital of France?"

You: "**Question**: What is the capital of France? **Answer**: Paris. **Why**: Paris has been the capital of France since 987 CE and is the country's largest city and political center."

Question: "Which of the following is a primary color? A) Green B) Red C) Purple D) Orange"

You: "**Question**: Which of the following is a primary color? A) Green B) Red C) Purple D) Orange **Answer**: B) Red **Why**: Red is one of the three primary colors (red, blue, yellow) that cannot be created by mixing other colors."

Question: "Solve for x: 2x + 5 = 13"

You: "**Question**: Solve for x: 2x + 5 = 13 **Answer**: x = 4 **Why**: Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4."`,

        outputInstructions: `**OUTPUT INSTRUCTIONS:**

Provide direct exam answers in **markdown format**. Include the question text, the correct answer choice, and a brief justification. Focus on efficiency and accuracy. Keep responses **short and to the point**.`,

    },

};

As the final line in however you make this prompt system work, tell the AI to respond with "I'm ready to help!" when it has context. This should be universal for every prompt even user created ones so make that an attachment appended to the bottom of all instructions sent out

While waiting for that message there should be an animated loading screen.

When loaded, then, a resizable, small-medium sized window pops up at the top of your screen as a little chat client at the top, right under where the webcam is on a laptop. The chatbox should have the returned chat from the AI in it which will be "I'm ready to help!". Text that shows up should always have a fast typing animation as it loads in. In this chatbox, there should be a textbox for the AI's responses, a chat for you to type and send messages by clicking the send button or pressing enter, an X button in the upper right hand corner to return to the homepage with buttons. There should also be a little transparency slider that should be set at 65% by default and go down to 10% at the top. It should be simple. It should be its own gui that you can drag around, not using the windows X and minimize button, its own style entirely.

How this software should work is that it should always be listening to the audio from the computer -- when there's silence or not words, it ignores. But when there is speaking coming from the interviewer, it listens and streams / records and uploads the interviewer's questions to Gemini -- the AI will parse the question, and return the answer to the textbox. You may need to research with perplexity MCP (you should research any questions you have and make that apart of the plans, remain in context to our stack and program) how to get this done; I'll include docs from a similar program outlining the functionality below in a second.

Another function is that every 2 seconds, a screenshot is taken. If the user types in and sends a prompt at any time, the photo is attached. I.e. if there's a math problem on the screen and the user prompts "Solve this math issue" The AI will return the answer in the chatbox. For the chatbox, it shouldnt show previous responses from the AI, only the current, but the AI's responses AND the voice transcript from the interviewer should be recorded for display in "Past Sessions" later. On top of that, if a prompt and photo is sent by the user, similarly the response from the AI and that should be recorded. 



Here's the rest of the pages / features but a bit less wordy:



PAST SESSIONS

When Past Sessions is clicked, a medium-sized window opens in the centre of the screen.

Session Table – a searchable, sortable table with these columns: • Date & Time • Profile Used • Session Title (auto-generated from the first user prompt) • Duration • Tags (editable)

Controls • Open – highlights the selected row and loads the full transcript, screenshots and AI replies in a right-hand preview pane. • Chat About Session – activates the specialised Gemini chat described earlier. The user must open a session first; otherwise the button is disabled. • Export PDF – saves the transcript, screenshots and AI replies to a single, timestamped PDF. • Delete – removes the session from the local SQLite DB after a confirmation modal. • Back – returns to the main menu.

Preview Pane – shows a scrollable timeline: • Interviewer speech (time-stamped, grey text) • User prompts (white text) • AI replies (accent colour text) • Screenshot thumbnails every 30 seconds – click to enlarge in a lightbox.

All session data (JSON transcript, WAV/FLAC audio chunks, PNG screenshots) is stored in ~/.clue-daddy/sessions/<UUID>/.

While the Chat About Session panel is active, the system prompt from Settings → AI is prepended with the full session transcript and any files originally used, then the model greets with “Hello! I’m ready to chat about your session. I have successfully received all context.”

CONTEXT BASE

Clicking Context Base opens a resizable window with a two-panel layout.

Left Sidebar – a list of profiles with a coloured icon indicating type (interview, sales, etc.). • Single click selects; double click edits. • Right-click shows a context menu: Duplicate, Rename, Delete, Export.

Right Panel – Profile Editor (visible when a profile is selected or New Profile is pressed):

Overview tab – profile name, type dropdown (pre-fills prompt examples), and a short description.

Context tab – a large markdown editor for free-form text, résumé snippets, etc.

Files tab – drag-and-drop area and Add Files button; accepted types: PDF, DOCX, TXT, PNG, JPG. Files copy into ~/.clue-daddy/profiles/<profile-id>/files/. PDFs are OCR-extracted to plain text automatically.

Custom Instructions tab – optional system-prompt overrides (markdown).

Perplexity tab – a single-line question box and Generate button that fetches an answer via the Perplexity API, appends it to the Context tab, and cites the source URL.

Top Bar Buttons • New Profile – opens a blank editor with a random accent colour. • Save – validates required fields, then writes profile.json. • Back – returns to main menu.

Profiles can be picked in Start Cheating via the dropdown; their JSON, files and custom instructions are bundled into the prompt payload sent to Gemini.

SETTINGS

Selecting Settings opens a tabbed preferences window.

General • Google Gemini API Key (masked input) • Personal Context (multiline text saved from onboarding) • Default Profile (dropdown) • Launch at System Start-up (checkbox)

Appearance • Accent Colour picker (defaults to teal) • Font Size slider (90 % – 120 %) • Window Transparency default (10 % – 90 %) • Enable Material Animations (toggle)

AI • Model selection (currently fixed to gemini-live-2.5-flash-preview, dropdown reserved for future) • Temperature (0 – 1) • Max Tokens per Reply (integer) • Universal System Prompt editor (markdown). The final line “I'm ready to help!” is appended automatically. • Search Tool Toggle – switch between built-in Google Search scraping or none. • Reset System Prompt to Default (button)

Hotkeys • Global Start Cheating shortcut (default: Ctrl + Shift + Space) • Transparency Increase / Decrease (default: Ctrl + Alt + Up/Down) • Quick Screenshot & Attach (default: Ctrl + Alt + S) • Restore Defaults (button)

Privacy & Data • Screenshot Frequency (seconds, default = 2) • Auto-Delete Sessions older than n days (toggle & integer) • Clear All Stored Data (danger zone) • View Log File (opens directory)

About • Version, licence, links to documentation and GitHub. • Check for Updates (button, pulls latest release info from GitHub API).

All settings are persisted to ~/.clue-daddy/config.json and re-loaded at start-up.

GLOBAL BACKGROUND SERVICES

These run once the app launches, irrespective of the visible page.

Audio Listener • Captures system audio with PyAudio, monitors RMS level to detect speech. • When speech exceeds threshold for > 300 ms, recording starts; it stops after 800 ms of silence. • Chunk is saved, transcribed with Google Speech-to-Text, then streamed to Gemini for a reply. • Non-speech periods are ignored to reduce cost.

Screenshot Capturer • Every X seconds (user-configurable), grabs the current full screen, compresses to PNG (80 % quality) and stores it in the active session folder. • When the user sends a manual prompt, the latest screenshot is attached to the API call.

Session Manager • Generates a UUID at the start of Start Cheating. • Creates a sub-directory and SQLite row; streams and writes transcript, screenshots, prompts and AI replies in real time. • Closes and finalises metadata when the chat window is dismissed.

All newly created pages and functions follow the same dark theme, rounded-corner design language and fast typing/slide-in animations established for the assistant window.

With these additions, every page, button and background process referenced in the original description is now fully specified.



Finally, I forgot to mention, for the "Add Profile" button, make it work by adding "Purpose", "Behavior", "Files", "Additional Context (text box)" and attach it to the system prompt when sent but write that system prompt to allow for that info to be used