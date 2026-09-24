===DOCUMENT UPLOADS===
1. Python data types
curl -s -X POST http://localhost:8000/api/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Data Types",
    "content": "Python has several built-in data types that are fundamental to programming.\n\nStrings are sequences of characters, created with single or double quotes. They are immutable, meaning once created they cannot be changed. Common string methods include .upper(), .lower(), .strip(), and .split().\n\nLists are ordered, mutable collections that can hold items of any type. You create them with square brackets: my_list = [1, 2, 3]. Lists support indexing, slicing, and methods like .append(), .pop(), and .sort().\n\nDictionaries are key-value pairs, created with curly braces: my_dict = {\"name\": \"Alice\", \"age\": 30}. Keys must be immutable (strings, numbers, tuples), but values can be any type. Access values with my_dict[\"name\"] or my_dict.get(\"name\").\n\nTuples are like lists but immutable. Once created, you cannot add or remove items. They are created with parentheses: my_tuple = (1, 2, 3). Tuples are often used for fixed collections of related values.\n\nSets are unordered collections of unique items. They are useful for removing duplicates and performing mathematical set operations like union, intersection, and difference."
  }' | jq


2. Land snails
curl -s -X POST http://localhost:8000/api/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Land Snails",
    "content": "Land snails are shelled gastropod mollusks adapted to life outside of water, found on every continent except Antarctica.\n\nAnatomy: A land snail'"'"'s body consists of a muscular foot used for locomotion, a head with two pairs of tentacles (the longer pair carries the eyes, the shorter pair senses touch and smell), and a coiled shell into which it can withdraw for protection. The shell grows in a spiral pattern as the snail ages, and its size and ridge count can help estimate the snail'"'"'s age.\n\nMovement and slime: Snails move by rippling muscular contractions along the foot, gliding over a layer of mucus they secrete. This slime reduces friction, protects the foot from sharp surfaces, and helps the snail retain moisture. Some species can even glide upside down or across a blade'"'"'s edge without injury because of it.\n\nDiet: Most land snails are herbivores or detritivores, feeding on leaves, algae, fungi, decaying plant matter, and sometimes soil for calcium. They use a rasping structure called a radula, lined with thousands of tiny teeth, to scrape food into digestible pieces.\n\nReproduction: Most land snails are hermaphrodites, possessing both male and female reproductive organs. Two snails typically still mate and exchange sperm to fertilize eggs, which are laid in small clutches in moist soil. Some species can self-fertilize if a mate is unavailable.\n\nHibernation and estivation: In cold or dry conditions, snails seal their shell opening with a dried mucus layer called an epiphragm and enter a dormant state — hibernation in winter, estivation in summer drought — to conserve moisture and survive until conditions improve."
  }' | jq



===TEST ENDPOINTS===

1. Create a conversation:
curl -s -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Python Basics Study Session"}' | jq

curl -s -X POST http://localhost:8000/api/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Snail Facts"}' | jq

2. Ask a question (replace '#' with the actual convo id):
curl -s -X POST http://localhost:8000/api/conversations/#/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the difference between a garden snail and a tuple?"}' | jq

curl -s -X POST http://localhost:8000/api/conversations/3/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "At what age do snails mature?"}' | jq

3. Ask a follow-up in the same conversation:
curl -s -X POST http://localhost:8000/api/conversations/#/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Can you give me an example of when I would use one instead?"}' | jq

curl -s -X POST http://localhost:8000/api/conversations/3/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Can you tell me at what age snails begin reproducing?"}' | jq

4. Compare — send the same follow-up to the history-free endpoint:
curl -s -X POST http://localhost:8000/api/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Can you give me an example of when I would use one instead?"}' | jq

curl -s -X POST http://localhost:8000/api/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Can you tell me at what age snails begin reproducing?"}' | jq

5. View the full conversation history:
curl -s http://localhost:8000/api/conversations/#/ | jq

6. Remove Document 1 and all its chunks/embeddings:
curl -X DELETE -i http://localhost:8000/api/documents/3/

7. Confirm it's gone
curl -s http://localhost:8000/api/documents/ | jq

8. Ask something that depended on it:
curl -s -X POST http://localhost:8000/api/conversations/1/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a list?"}' | jq