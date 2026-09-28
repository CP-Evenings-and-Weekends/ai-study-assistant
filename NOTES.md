QUESTION 1
----------
curl -s -X POST http://localhost:8000/api/ask/ -H "Content-Type: application/json" \
  -d '{"question": "How do I create a Python list?"}' | jq

{
  "answer": "According to the provided context, you create a Python list with square brackets: `my_list = [1, 2, 3]`.",
  "sources": [
    {
      "title": "Python Data Types v2",
      "preview": "Python has several built-in data types that are fundamental to programming.\n\nStrings are sequences of characters, created with single or double quotes. They are immutable, meaning once created they ca",
      "relevance_score": 0.6608
    },
    {
      "title": "Python Data Types v2",
      "preview": "Tuples are like lists but immutable. Once created, you cannot add or remove items. They are created with parentheses: my_tuple = (1, 2, 3). Tuples are often used for fixed collections of related value",
      "relevance_score": 0.4967
    },
    {
      "title": "The Water Cycle",
      "preview": "The water cycle describes how water moves continuously through Earth and its atmosphere in a repeating cycle.\n\nEvaporation occurswhen the sun heats water in oceans, lakes, and rivers, turning it into",
      "relevance_score": 0.4209
    },
    {
      "title": "The Water Cycle",
      "preview": "Collection is the final stage, where precipitation gathers in oceans, lakes, rivers, and underground aquifers. Some of this water eventually evaporates again, restarting the cycle, while some is absor",
      "relevance_score": 0.4161
    }
  ]
}


QUESTION 2
----------
curl -s -X POST http://localhost:8000/api/ask/ -H "Content-Type: application/json" \
  -d '{"question": "What causes clouds to form?"}' | jq

{
  "answer": "According to the context, clouds form when water vapor in the atmosphere cools, turning back into tiny liquid droplets. This process is described as condensation, which happens when water vapor rises into the atmosphere and cools as it rises.",
  "sources": [
    {
      "title": "The Water Cycle",
      "preview": "The water cycle describes how water moves continuously through Earth and its atmosphere in a repeating cycle.\n\nEvaporation occurswhen the sun heats water in oceans, lakes, and rivers, turning it into",
      "relevance_score": 0.701
    },
    {
      "title": "The Water Cycle",
      "preview": "Collection is the final stage, where precipitation gathers in oceans, lakes, rivers, and underground aquifers. Some of this water eventually evaporates again, restarting the cycle, while some is absor",
      "relevance_score": 0.6059
    },
    {
      "title": "Python Data Types v2",
      "preview": "Tuples are like lists but immutable. Once created, you cannot add or remove items. They are created with parentheses: my_tuple = (1, 2, 3). Tuples are often used for fixed collections of related value",
      "relevance_score": 0.416
    },
    {
      "title": "Python Data Types v2",
      "preview": "Python has several built-in data types that are fundamental to programming.\n\nStrings are sequences of characters, created with single or double quotes. They are immutable, meaning once created they ca",
      "relevance_score": 0.3682
    }
  ]
}


QUESTION 3
----------
curl -s -X POST http://localhost:8000/api/ask/ -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of Japan?"}' | jq

"answer": "There is no information in the provided context about the capital of Japan. The context only discusses the water cycle and Python data types."


QUESTION 4
----------
curl -s -X POST http://localhost:8000/api/ask/ -H "Content-Type: application/json" \
  -d '{"question": "What is a set?"}' | jq

{
  "answer": "A set is an unordered collection of unique items.",
  "sources": [
    {
      "title": "Python Data Types v2",
      "preview": "Tuples are like lists but immutable. Once created, you cannot add or remove items. They are created with parentheses: my_tuple = (1, 2, 3). Tuples are often used for fixed collections of related value",
      "relevance_score": 0.6095
    },
    {
      "title": "Python Data Types v2",
      "preview": "Python has several built-in data types that are fundamental to programming.\n\nStrings are sequences of characters, created with single or double quotes. They are immutable, meaning once created they ca",
      "relevance_score": 0.4928
    },
    {
      "title": "The Water Cycle",
      "preview": "Collection is the final stage, where precipitation gathers in oceans, lakes, rivers, and underground aquifers. Some of this water eventually evaporates again, restarting the cycle, while some is absor",
      "relevance_score": 0.4389
    },
    {
      "title": "The Water Cycle",
      "preview": "The water cycle describes how water moves continuously through Earth and its atmosphere in a repeating cycle.\n\nEvaporation occurswhen the sun heats water in oceans, lakes, and rivers, turning it into",
      "relevance_score": 0.4299
    }
  ]
}


QUESTION 5
----------
curl -s -X POST http://localhost:8000/api/ask/ -H "Content-Type: application/json" \
  -d '{"question": "What does collection mean?"}' | jq

{
  "answer": "In the context provided, \"collection\" refers to a gathering of items, such as precipitation gathering in oceans, lakes, rivers, and underground aquifers.",
  "sources": [
    {
      "title": "The Water Cycle",
      "preview": "Collection is the final stage, where precipitation gathers in oceans, lakes, rivers, and underground aquifers. Some of this water eventually evaporates again, restarting the cycle, while some is absor",
      "relevance_score": 0.6483
    },
    {
      "title": "Python Data Types v2",
      "preview": "Tuples are like lists but immutable. Once created, you cannot add or remove items. They are created with parentheses: my_tuple = (1, 2, 3). Tuples are often used for fixed collections of related value",
      "relevance_score": 0.5254
    },
    {
      "title": "The Water Cycle",
      "preview": "The water cycle describes how water moves continuously through Earth and its atmosphere in a repeating cycle.\n\nEvaporation occurswhen the sun heats water in oceans, lakes, and rivers, turning it into",
      "relevance_score": 0.472
    },
    {
      "title": "Python Data Types v2",
      "preview": "Python has several built-in data types that are fundamental to programming.\n\nStrings are sequences of characters, created with single or double quotes. They are immutable, meaning once created they ca",
      "relevance_score": 0.4537
    }
  ]
}