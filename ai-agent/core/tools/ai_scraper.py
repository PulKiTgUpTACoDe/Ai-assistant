from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, BrowserProfile, Controller
from dotenv import load_dotenv
from typing import Any, Optional
import re

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

browser_profile = BrowserProfile(
    executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    headless=False,
    args=[
        '--disable-gpu',
        '--no-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials'
    ]
)

browser_session = BrowserSession(
    browser_profile=browser_profile,
)

def split_content(content: list, max_chunk_size: int = 4000) -> list:
    """Split content into smaller chunks while trying to preserve sentence boundaries.
    Args:
        content: List of content items from the agent (final_result, action_results, extracted_content)
        max_chunk_size: Maximum size of each chunk in characters
    Returns:
        List of processed chunks
    """
    chunks = []
    
    # Process each item in the content list
    for item in content:
        if not item:  # Skip empty items
            continue
            
        # Convert item to string if it's not already
        item_text = str(item)
        
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', item_text)
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size + sentence_size > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
    
    return chunks

async def web_automation_task(url: Optional[str], task: str = "extract all content") -> Any:
    
    try:
        agent = Agent(
            task=f"{task} from {url}",
            llm=llm,
            browser_session=browser_session,
        )

        raw_agent_output = await agent.run()
        raw_result = [raw_agent_output.action_results(), raw_agent_output.extracted_content(), raw_agent_output.final_result()]
        
        # Split content into manageable chunks
        content_chunks = split_content(raw_result)
        
        # Summarize each chunk
        chunk_summaries = []
        for chunk in content_chunks:
            summary_prompt = f"""Please provide all the meaningful content from the following content while preserving the key information and meaning. 
            Focus on the most important points and maintain the essential context. Here's the content:
            
            {chunk}
            """
            
            summary_response = llm.invoke(summary_prompt)
            chunk_summaries.append(summary_response.content)
        
        # Combine all chunk summaries
        combined_summary = "\n\n".join(chunk_summaries)
        
        # Final summary of all chunk summaries
        final_summary_prompt = f"""Please provide a final concise summary of the following content chunks. 
        Combine the key points while eliminating redundancy and maintaining a coherent narrative:
        
        {combined_summary}
        """
        
        final_summary = llm.invoke(final_summary_prompt)
        return final_summary.content

    except Exception as e:
        return f"An error occurred during web automation: {e}"
