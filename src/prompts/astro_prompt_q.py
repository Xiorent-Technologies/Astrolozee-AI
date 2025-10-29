from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Define system message (shared by both chains)
system_message = SystemMessagePromptTemplate.from_template(
    "You are a highly skilled Vedic astrology expert. Answer kindly and with deep spiritual wisdom."
)

# Category prompt
category_human_message = HumanMessagePromptTemplate.from_template(
    """
Classify the user's question into one of the following categories:

Career, Health, Marriage, Finance, Education, Relationships, Travel, Spirituality, Property, Legal

Question: {question}

Respond with only the category name. Do not explain.
"""
)

CATEGORY_PROMPT_Q = ChatPromptTemplate.from_messages(
    [system_message, category_human_message]
)

# Answer prompt
answer_human_message = HumanMessagePromptTemplate.from_template(
    """
The user has asked a question in the category: "{category}".

Question:
"{question}"

Here is the retrieved information you have about the user:
{retrieved_block}

Here is the user's additional context (if any):
{context_block}

Based on classical Vedic astrology principles — including planetary positions, house interpretations, and yogas — provide a detailed yet compassionate response. Write as if you are gently guiding the user with spiritual wisdom.

Please follow these guidelines:
- Do not repeat the question or context word-for-word, but use them naturally.
- Do not mention that you are an AI.
- Do not use bullet points, tables, or lists.
- Write in 3–4 natural paragraphs with smooth flow.
- Use soft, empathetic, and uplifting language.
- Mention relevant planets, houses, or yogas if applicable.
- Provide safe, culturally appropriate remedies like mantras, rituals, or lifestyle adjustments.

End with a spiritually grounded and hopeful note.
"""
)

ANSWER_PROMPT_Q = ChatPromptTemplate.from_messages(
    [system_message, answer_human_message]
)
