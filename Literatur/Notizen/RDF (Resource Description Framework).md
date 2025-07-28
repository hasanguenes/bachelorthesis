---
title: Allgemeines zu RDF
date: 30.05.2025
---
Links: 
- https://www.w3.org/TR/rdf-primer/
- https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/#resources-and-statements

RDF is a framework for expressing information in the Web.

---
#ChatGPT https://chatgpt.com/g/g-p-6825c5af5d68819194daff1297549bd2-hasi-ba/c/6839cf9d-f59c-8005-be80-88b860ab3c77
- **RDF** ist das **Grundgerüst** für Aussagen in Form von Tripeln.
- **RDFS** baut darauf auf und ermöglicht die Beschreibung von **Strukturen und Regeln** innerhalb der Daten.
---
# Graph-based Data Model

Graph consists of set of triples: subject, predicate, object. 
Set of triples = RDF graph
An RDF graph can be visualized as a graph with vertices being subject or object and edges being the predicate.

3 kinds of nodes:
- IRI
- Literal
- Blank Node

IRIs, literals and blank nodes are collectively known as **RDF terms**.
An RDF **term n** has a **value v for property p** in an RDF graph if there is an RDF triple in the graph with **subject n**, **predicate p**, and **object v**.

**Predicate** is of an **IRI** and denotes a **property**.

# Resources and Statements

**IRI** or **Literal** denotes something in the world. These things are called [[Resources]].  
Asserting an RDF triple says that some relationship, indicated by the predicate, holds between the resources denoted by the subject and object. This statement corresponding to an RDF triple is known as an **RDF statement**.  

**Blank Nodes** don't identify specific resources. Statements involving blank nodes say that something with the given relationships exists, without explicitly naming it.

---
# RDF Data Model

## Triples

An RDF Statement is called triple and consists of following structure:

``` <subject> <predicate> <object> ```

The relationship is phrased in a directional way from subject to object and is called a **property**.

Example RDF triples:
``
```
<Bob> <is a> <person>.
<Bob> <is a friend of> <Alice>.
<Bob> <is born on> <the 4th of July 1990>. 
<Bob> <is interested in> <the Mona Lisa>.
<the Mona Lisa> <was created by> <Leonardo da Vinci>.
<the video 'La Joconde à Washington'> <is about> <the Mona Lisa>
```

---
# IRIs
IRI is short for *International Resource Identifier* and identifies a [[Resources]]. 
For example: URL
**IRIs** can appear in **all 3 positions** of a triple.
IRIs are global identifiers, so other people can re-use this IRI to identify the same thing.

---
# Literals

Literals are basic values that are not IRIs. 
For example: 
- sting like "La Joconde"
- date like "the 4th of July, 1990"
Literals are associated with a datatype enabling such values to be parsed and interpreted correctly. 
Literals may only appear in the **object** position.

---
# Blank Nodes
In addition, it is sometimes handy to be able to talk about resources without bothering to use a global identifier.
Blank nodes are like simple variables in algebra; they represent some thing without saying what their value is.
Blank nodes can appear in the **subject and object** position of a triple. They can be used to denote resources without explicitly naming them with an IRI.

---
# Multiple Graphs
RDF provides a mechanism to group RDF statements in multiple graphs and associate such graphs with an IRI.
Multiple graphs in an RDF document constitute an **RDF dataset**.  
An RDF dataset may have multiple named graphs and at most one unnamed ("default") graph.

---
# RDF Vocabularies 