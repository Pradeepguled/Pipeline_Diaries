# STORY : 3

## Simplifying HL7 Log Search Using Meaning-Based Queries

### Questions :

* Tell me about a time when you **thought big** and went beyond the existing system.
* Tell me about a time when you **invented a new solution** to solve a problem.
* Tell me about a time when you **simplified a complex system** for users.
* Tell me about a time when you **improved a user experience** significantly.
* Tell me about a time when you  **took initiative without being asked** .


## STAR + LEARNING :

### **Situation**

There was an existing **UI** where users searched **HL7 logs** using  **text-based keyword search** .

To find information, users had to:

* Know exact **HL7 codes or keywords**
* Try multiple searches
* Manually scan through logs

This worked technically, but it was  **slow and frustrating** , especially for users who didn’t know HL7 message formats.

### **Task**

I wanted to **improve the search experience** so users could find information  **based on meaning** , not exact text.

My goal was to:

* Reduce dependency on HL7 technical knowledge
* Make search faster and more intuitive
* Simplify how users interact with complex log data

There were no clear requirements for this — it was an  **initiative I took on my own** .

---

### **Action**

I designed and built a  **meaning-based search solution** .

* I converted HL7 logs into **readable text chunks**
* Generated **embeddings** so the system could understand the **intent and meaning** of the logs
* Stored them in a **vector database**
* Updated the UI so users could ask **natural language questions**

For example:

* Instead of searching `ADT^A01`, users could ask

  *“show patient admissions today”*
* Instead of searching `OBX|Hemoglobin`, users could ask

  *“show patients with low hemoglobin”*

I made sure the solution was  **simple for users** , even though the backend logic was complex.

---

### **Result**

* Search became **faster and easier**
* Users no longer needed deep HL7 knowledge
* Fewer retries and less manual effort were needed
* The UI became more user-friendly and intuitive
* The solution showed clear value as an **improvement over keyword search**

---

### **Learning**

This initiative taught me that  **complex data does not need complex user experience** .

I learned that:

* Thinking beyond existing workflows can unlock big improvements
* New technologies like embeddings are powerful when used  **to simplify** , not to impress
* Building something useful starts with understanding  **user pain** , not tools

Since then, I always look for opportunities to  **simplify how users interact with complex systems** .

---

### **One-Line Summary**

> I replaced keyword-based HL7 search with meaning-based search so users could find answers using natural language instead of technical codes.

---

### Why this is a STRONG Amazon story

* ✅ Think Big
* ✅ Invent and Simplify
* ✅ Initiative and Ownership
* ✅ Clear user impact
* ✅ Simple and explainable
