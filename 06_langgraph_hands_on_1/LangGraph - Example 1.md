# LangGraph - Example 1

A Gentle Introduc.on to LangGraph
     A Step-by-Step Tutorial

         A Quick Overview
       Instructor: A. Namin

                                    1

           What is LangGraph?
• DeﬁniAon:
  – An orchestraAon framework for building complex
    agenAc systems
• Key CharacterisAcs:
  – Low-level control: More granular than LangChain
    agents
  – Determinis.c ﬂows: Pre-deﬁned execuAon paths
    guaranteed every Ame
  – Graph-based: Workﬂows represented as directed
    graphs with nodes and edges
  – State management: Structured state shared across all
    nodes
                                                       2

         LangGraph vs LangChain
• LangChain Agents:
   – Dynamic reasoning at runAme
   – Plan changes based on observaAons
   – Less control over execuAon ﬂow
   – Good for exploratory tasks
• LangGraph:
   – Pre-deﬁned workﬂow structure
   – Guaranteed execuAon path
   – Full control over ﬂow ProducAon-ready determinism
• Key Insight:
   – Use LangGraph when you need predictable, controlled
     workﬂows that must follow speciﬁc business logic every Ame.

                                                                   3

     Core Concepts in LangGraph
• 1. State
   – A shared data structure (TypedDict) that ﬂows through the
     graph
• 2. Nodes
   – FuncAons that process and update the state
• 3. Edges
   – ConnecAons deﬁning ﬂow between nodes
• 4. CondiAonal Edges
   – Decision points that route to diﬀerent nodes based on
     condiAons
• 5. Graph Builder
   – Tool to construct and compile the workﬂow.

                                                             4

          Best PracAce - Bo\om-Up
                Development
• Step-by-Step Workﬂow:
   – Step 1: Draw the graph on paper ﬁrst
   – Step 2: Deﬁne nodes using add_node()
   – Step 3: Create edges with add_edge()
   – Step 4: Add condiAonal edges if needed
   – Step 5: Deﬁne the State class
   – Step 6: Implement node funcAons
   – Step 7: Compile and visualize
   – Step 8: Test and iterate
• Pro Tip: Always start with a visual diagram. It helps you
  think through the logic before wriAng code.
                                                          5

Tutorial Example - Customer Feedback
             Processor
•   Business Problem:
     –   Process social media comments to idenAfy quesAons vs compliments and route them appropriately
•   Workﬂow Overview:

START
 ↓
Extract Content
 ↓
Route (QuesAon/Compliment)
 ↓ QuesAon → Run QuesAon Code
 ↓ Compliment → Run Compliment Code
 ↓
BeauAfy
 ↓
END

Input: API payload with customer remarks, Amestamps, social media channel, etc.

                                                                                                         6

         Step 1 - CreaAng Nodes Code
               ImplementaAon
from langgraph.graph import StateGraph

graph_builder = StateGraph(State)

# Add all nodes
graph_builder.add_node("extract_content", extract_content)
graph_builder.add_node("run_quesAon_code", run_quesAon_code)
graph_builder.add_node("run_compliment_code", run_compliment_code)
graph_builder.add_node("beauAfy", beauAfy)

Important Notes:
• START and END nodes are built-in (no need to create them)
• First argument = node name (string)
• Second argument = Python funcAon name
• Names can diﬀer but keeping them idenAcal improves readability

                                                                     7

Step 2 - CreaAng Standard Edges Code
            ImplementaAon
from langgraph.graph import END, START

# Deﬁne edges (connecAons between nodes)
graph_builder.add_edge(START, "extract_content")
graph_builder.add_edge("run_quesAon_code", "beauAfy")
graph_builder.add_edge("run_compliment_code", "beauAfy")
graph_builder.add_edge("beauAfy", END)

•   What are Edges?
    – Edges deﬁne the ﬂow of execuAon from one node to another. They create the graph
      structure.
•   Remember:
    – Use node names (strings), not funcAon names when adding edges!

                                                                                        8

    Step 3 - CreaAng CondiAonal Edges
              ImplementaAon
graph_builder.add_condiAonal_edges(
  "extract_content",      # Source node
  route_quesAon_or_compliment, # RouAng funcAon
  {
     "compliment": "run_compliment_code",
     "quesAon": "run_quesAon_code",
  },
)

Three Required Arguments:
1. Source node: Where the condiAonal check happens
2. RouAng funcAon: Contains condiAonal logic, returns a string
3. Route mapping: DicAonary mapping return values to target nodes

Key Point: The rouAng funcAon must return one of the keys in the mapping dicAonary.

                                                                                      9

         Step 4 - Deﬁning the State Class
                 ImplementaAon
from typing_extensions import TypedDict

class State(TypedDict):
   text: str            # Extracted content
   answer: str             # Final response
   payload: dict[str, list] # Input data

•   State Purpose:
     –   Centralized data storage: All variables accessible across nodes
     –   Type safety: TypedDict provides type hints
     –   Data ﬂow: InformaAon passes between nodes via state
     –   Immutability: Each node returns updated values, doesn't mutate directly
•   Best PracAce: Deﬁne all variables you'll need upfront in the State class.

                                                                                   10

    Step 5 - ImplemenAng Node FuncAons (Part 1)
                                        ImplementaAon
•    Extract Content Node:

def extract_content(state: State):
  # Access payload from state
  # Extract customer_remark ﬁeld
  return {"text": state["payload"][0]["customer_remark"]}

•    RouAng FuncAon:

def route_quesAon_or_compliment(state: State):
  if "?" in state["text"]:
     return "quesAon"
  else:
     return "compliment”

Pa\ern: Every node funcAon:
Takes state: State as parameter
Returns a dicAonary with updated state variables            11
Accesses exisAng state via state["variable_name"]

    Step 5 - ImplemenAng Node FuncAons (Part 2)
                             ImplementaAon
•   AcAon Nodes:

def run_compliment_code(state: State):
  return {"answer": "Thanks for the compliment."}

def run_quesAon_code(state: State):
  return {"answer": "Wow nice quesAon."}

•   BeauAfy Node:

def beauAfy(state: State):
  # Access current answer and modify it
  return {"answer": state["answer"] + " beauAﬁed"}

Note: By default, returning a dicAonary with an exisAng key overwrites that variable in the state.
We'll learn how to append instead in upcoming slides.

                                                                                                 12

         Step 6 - Compiling and Visualizing
           Code to Compile and Display
# Compile the graph
graph = graph_builder.compile()

# Visualize the graph
from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))

•   Visual Indicators:
     –   Solid Edges: Always executed in the workﬂow
     –   Do\ed Edges: CondiAonal - only one branch executes
•   Pro Tip: Always visualize your graph before running to verify the structure matches your
    design.

                                                                                               13

             Step 7 - ExecuAng the Graph
Using invoke():

result = graph.invoke({
   "payload": [{
      "Ame_of_comment": "20-01-2025",
      "customer_remark": "I hate this.",
      "social_media_channel": "facebook",
      "number_of_likes": 100,
   }]
})

# Output shows ﬁnal state
print(result)

Output Example:
{
  'text': 'I hate this.',
  'answer': 'Thanks for the compliment. beauAﬁed',
  'payload': [...]
}

invoke() returns: The complete ﬁnal state auer graph execuAon
                                                                14

 Monitoring ExecuAon - Using stream()
for step in graph.stream({
    "payload": [{
       "customer_remark": "I hate this.",
       ...
    }]
}):
    print(step)

Output (step-by-step):

{'extract_content': {'text': 'I hate this.'}}
{'run_compliment_code': {'answer': 'Thanks for the compliment.'}}
{'beauAfy': {'answer': 'Thanks for the compliment. beauAﬁed'}}

Use Case: stream() is perfect for:
•   Showing progress bars in UI
•   Debugging node-by-node execuAon
•   Real-Ame updates to users

                                                                    15

    Advanced - Appending vs OverwriAng
                  State
The Problem: By default, updaAng a state variable overwrites its value. SomeAmes you want to
append instead.
SoluAon: Annotated Types

from typing import Annotated
import operator

class State(TypedDict):
   text: str
   # Changed from str to list with operator.add
   answer: Annotated[list, operator.add]
   payload: dict[str, list]

•   Annotated Format: Annotated[data_type, operator]
     – operator.add works with lists, strings, and numbers
     – Each return value gets appended instead of replacing

                                                                                               16

 UpdaAng FuncAons for Appending
Modiﬁed Node FuncAons:

def run_compliment_code(state: State):
  # Return list instead of string
  return {"answer": ["Thanks for the compliment."]}

def run_quesAon_code(state: State):
  return {"answer": ["Wow nice quesAon."]}

Modiﬁed BeauAfy FuncAon:

def beauAfy(state: State):
  # Access last item in list
  last_answer = state["answer"][-1]
  return {"answer": [last_answer + " beauAﬁed"]}

Result: Now answer contains both intermediate and ﬁnal values: ['Thanks for the compliment.', 17
'Thanks for the compliment. beauAﬁed']

  Custom Operators for Complex Types
The Problem: operator.add doesn't work with dicAonaries. For complex data structures, you
need custom merge logic.

CreaAng a Custom Operator:

def merge_dicts(dict1, dict2):
  # Merge two dicAonaries
  return {**dict1, **dict2}

class State(TypedDict):
   text: str
   answer: Annotated[dict, merge_dicts] # Custom operator
   payload: dict[str, list]

Power Tip: You can create custom operators for any complex merge logic - nested dicAonaries,
custom objects, etc.

                                                                                               18

Using Custom Operators in PracAce
Updated Node FuncAons:

def run_compliment_code(state: State):
  return {"answer": {"temp_answer": "Thanks for the compliment."}}

def beauAfy(state: State):
  return {
    "answer": {
      "ﬁnal_beauAﬁed_answer":
         state["answer"]["temp_answer"] + " beauAﬁed"
    }
  }

                                                                     19

Using Custom Operators in PracAce
Final Output:

{
    'answer': {
      'temp_answer': 'Thanks for the compliment.',
      'ﬁnal_beauAﬁed_answer': 'Thanks for the compliment. beauAﬁed'
    }
}

                                                                      20

 Parallel Node ExecuAon - Use Case
New Requirement: Tag the type of customer remark (packaging, sustainability, medical) while
determining if it's a quesAon or compliment.

Enhanced Workﬂow:

START
 ↓
Extract Content
 ↓ (parallel execuAon)
 ├─→ Tag Query → ┐
 └─→ Route      → BeauAfy → END
   ↓ QuesAon → Run QuesAon Code ↑
   ↓ Compliment → Run Compliment Code ↑

Beneﬁt: Nodes execute concurrently in the same superstep for eﬃciency.

                                                                                              21

    ImplemenAng Parallel ExecuAon
Add New Node and Edge:

graph_builder.add_node("tag_query", tag_query)
graph_builder.add_edge("tag_query", "beauAfy")

Tag Query FuncAon:

def tag_query(state: State):
  if "package" in state["text"]:
     return {"tag": "Packaging"}
  elif "price" in state["text"]:
     return {"tag": "Pricing"}
  else:
     return {"tag": "General"}

                                                 22

    ImplemenAng Parallel ExecuAon
Update State:

class State(TypedDict):
   text: str
   tag: str # New variable
   answer: Annotated[dict, merge_dicts]
   payload: dict[str, list]

                                          23

                   Using Parallel Results
Updated BeauAfy FuncAon:

def beauAfy(state: State):
  return {
     "answer": {
       "ﬁnal_beauAﬁed_answer":
          state["answer"]["temp_answer"] +
          f' I will pass it to the {state["tag"]} Department'
     }
  }
Final Output:
{
  'tag': 'General',
  'answer': {
     'ﬁnal_beauAﬁed_answer':
       'Thanks for the compliment. I will pass it to the General Department'
  }                                                                            24
}

                  Advanced LLM IntegraAon
Enhanced RouAng with LLM

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = AzureChatOpenAI(
   deployment_name="gpt-4o",
   model_name="gpt-4o",
   temperature=0.1,
)

template = """
I have a piece of text: {text}.
Tell me whether it is a 'compliment' or a 'quesAon'.
"""

prompt = ChatPromptTemplate([("user", template)])
chain = prompt | llm | StrOutputParser()

def route_quesAon_or_compliment(state: State):
  response = chain.invoke({"text": state["text"]})
  return response
                                                            25

                          Key Takeaways
Core Principles:
1. Start with a diagram - visualize before coding
2. State is central - all data ﬂows through it
3. Nodes are funcAons - they transform state
4. Edges deﬁne ﬂow - control execuAon order
5. CondiAonal edges - enable decision making
6. Operators control merging - append vs overwrite

When to Use LangGraph:
• ProducAon workﬂows requiring determinisAc execuAon
• Complex mulA-step AI agent workﬂows
• When you need full control over execuAon ﬂow
• Building reliable, reproducible AI systems:

                                                       26

           Next Steps and Resources
What We Covered:
• Basic graph construcAon
• State management ? CondiAonal rouAng
• Custom operators
• Parallel execuAon
• LLM integraAon

Next Steps:
• Part 2: RAG-based workﬂows with LangGraph
• Using the Send API for advanced map-reduce pa\erns
• Building producAon-ready AI agents
• ImplemenAng human-in-the-loop workﬂows

Resources:
• GitHub: V-Sher/LangGraphTutorial LangChain
• DocumentaAon: docs.langchain.com
• Original ArAcle: levelup.gitconnected.com            27

         HANDS-ON EXERCISE SLIDES
EXERCISE 1: Build Your First Graph

Task: Create a simple graph that:
1. Takes a customer email as input
2. Classiﬁes it as "urgent" or "rouAne"
3. Routes to diﬀerent response nodes
4. Combines ﬁnal response

Hints:
• Use 4 nodes: classify, urgent_response, rouAne_response, format_output
• Use condiAonal edge auer classify
• Test with sample emails

                                                                           28

         HANDS-ON EXERCISE SLIDES
EXERCISE 2: Implement State Appending

Task: Modify the graph to:
1. Keep track of all processing steps
2. Store intermediate results
3. Return complete history

Requirements:
• Use Annotated[list, operator.add]
• Each node should append to history
• Final output shows full processing chain

                                             29

         HANDS-ON EXERCISE SLIDES
EXERCISE 3: Create Custom Operator

Task: Build a custom operator that:
1. Merges nested dicAonaries intelligently
2. Handles conﬂicts by keeping most recent value
3. Maintains metadata Amestamps

def smart_merge(dict1, dict2):
  # Your implementaAon here
  pass

                                                   30

          HANDS-ON EXERCISE SLIDES
EXERCISE 4: Parallel Processing

Task: Create a graph that processes data in parallel:
1. Extract content from input
2. Simultaneously: (a) Analyze senAment, (b) Extract keywords, (c) Detect language
3. Combine all results in ﬁnal node

Bonus: Add Aming informaAon to see parallel speedup

                                                                                     31

                    DEBUGGING TIPS
Common Issues:
1. State variables not updaAng
    1. Check you're returning dicAonary from funcAons
    2. Verify variable names match State class
2. CondiAonal edge errors
    1. Ensure rouAng funcAon returns exact key from mapping
    2. Check for typos in node names
3. Graph visualizaAon shows unexpected ﬂow
    1. Review edge deﬁniAons
    2. Verify condiAonal logic
4. Import errors
    1. Install: pip install langgraph langchain
    2. Check Python version (3.9+)

                                                              32

                                                      Complete Code
from typing_extensions import TypedDict
from typing import Annotated
import operator
from langgraph.graph import StateGraph, END, START

# Deﬁne State
class State(TypedDict):
   text: str
   answer: Annotated[list, operator.add]
   payload: dict[str, list]

# Deﬁne node funcAons
def extract_content(state: State):
  return {"text": state["payload"][0]["customer_remark"]}

def route_quesAon_or_compliment(state: State):
  if "?" in state["text"]:
     return "quesAon"
  else:
     return "compliment"

def run_compliment_code(state: State):
  return {"answer": ["Thanks for the compliment."]}

def run_quesAon_code(state: State):
  return {"answer": ["Wow nice quesAon."]}

def beauAfy(state: State):
  return {"answer": [state["answer"][-1] + " beauAﬁed"]}

# Build graph
graph_builder = StateGraph(State)

# Add nodes                                                           33
graph_builder.add_node("extract_content", extract_content)

                                  References
•   Gentle Introduc.on to LangGraph: A Step-by-Step Tutorial (Dr. Varshita Sher)
     – h\ps://levelup.gitconnected.com/gentle-introducAon-to-langgraph-a-step-by-step-
         tutorial-2b314c967d3c?gi=•ded980ec3f
•   Cloud LLM used for slides generaAon

                                                                                         34
