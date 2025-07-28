---
title: Allgemeines zu SHACL
date: 30.05.2025
---
Links:
- https://www.w3.org/TR/2017/REC-shacl-20170720/

SHACL is a language for validating RDF graphs against a set of conditions.
These conditions are provided as shapes and other constructs expressed in the form of an RDF graph. RDF graphs that are used in this manner are called **shapes graphs** in SHACL and the RDF graphs that are validated against a shapes graph are called **data graphs**. As SHACL shape graphs are used to validate that data graphs satisfy a set of conditions they can also be viewed as a description of the data graphs that do satisfy these conditions.

Nodes in an RDF graph that are subclasses, superclasses, or types of nodes in the graph are referred to as **SHACL class**.
A node n in an RDF graph G is a **SHACL instance** of a SHACL class C in G if one of the SHACL types of n in G is C.
An RDF term that is validated against a shape using the triples from a data graph is called a **focus node**.
A **constraint component** is an IRI. Each constraint component has one or more **mandatory** parameters, each of which is a property. Each constraint component has zero or more **optional** parameters, each of which is a property. The parameters of a constraint component are its mandatory parameters plus its optional parameters.

---
# SHACL Example
Example **data graph** with 3 SHACL instances of the class ``ex:Person``:
```
ex:Alice
	a ex:Person ;
	ex:ssn "987-65-432A" .
  
ex:Bob
	a ex:Person ;
	ex:ssn "123-45-6789" ;
	ex:ssn "124-35-6789" .
  
ex:Calvin
	a ex:Person ;
	ex:birthDate "1971-07-07"^^xsd:date ;
	ex:worksFor ex:UntypedCompany .
```

Example shows following conditions:
- A SHACL instance of ``ex:Person`` can have at most one value for the property ``ex:ssn``, and this value is a literal with the datatype ``xsd:string`` that matches a specified regular expression.
- A SHACL instance of ``ex:Person`` can have unlimited values for the property ``ex:worksFor``, and these values are IRIs and SHACL instances of ``ex:Company``.
- A SHACL instance of ``ex:Person`` cannot have values for any other property apart from ``ex:ssn``, ``ex:worksFor`` and ``rdf:type``.
The aforementioned conditions can be represented as shapes and constraints in the following **shapes graph**:
```
ex:PersonShape
	a sh:NodeShape ;
	sh:targetClass ex:Person ;    # Applies to all persons
	sh:property [                 # _:b1
		sh:path ex:ssn ;           # constrains the values of ex:ssn
		sh:maxCount 1 ;
		sh:datatype xsd:string ;
		sh:pattern "^\\d{3}-\\d{2}-\\d{4}$" ;
	] ;
	sh:property [                 # _:b2
		sh:path ex:worksFor ;
		sh:class ex:Company ;
		sh:nodeKind sh:IRI ;
	] ;
	sh:closed true ;
	sh:ignoredProperties ( rdf:type ) .
```

The prefix `sh` stands for the SHACL-namespace and refers to terms from the SHACL language. Typically, `sh` is defined as `@prefix sh: <http://www.w3.org/ns/shacl#> `  


We can use the shape declaration above to illustrate some of the key terminology used by SHACL. The target for the shape ``ex:PersonShape ``is the set of all SHACL instances of the class ``ex:Person``. This is specified using the property`` sh:targetClass``. During the validation, these target nodes become focus nodes for the shape. The shape ``ex:PersonShape`` is a node shape, which means that it applies to the focus nodes. It declares constraints on the focus nodes, for example using the parameters ``sh:closed`` and ``sh:ignoredProperties``. The node shape also declares two other constraints with the property ``sh:property``, and each of these is backed by a property shape. These property shapes declare additional constraints using parameters such as ``sh:datatype`` and ``sh:maxCount``.

In this example for the `ssn` property:
- `sh:path ex:ssn` -> restrictions are valid for ssn (`path` is a predicate which indicates which rdf-paths have to be validated)
- ``sh:maxCount 1`` -> at most one `ssn` per person
- `sh: datatype xsd: string` -> the value has to be of type string
- `sh:pattern "^\\d{3}-\\d{2}-\\d{4}$"` ->  string has to fit in the US-ssn scheme, f.e. 123-45-6789

In this example for the  `worksFor` property:
- `sh:class ex:Company` -> object with this property has to be an instance of class `ex:Company` 
- `sh:nodeKind sh:IRI` -> The object must be an IRI, not a blank node or literal

Some of the property shapes specify parameters from multiple constraint components in order to restrict multiple aspects of the property values. For example, in the property shape for ``ex:ssn``, parameters from three constraint components are used. The parameters of these constraint components are ``sh:datatype``, ``sh:pattern`` and ``sh:maxCount``. For each focus node the property values of ``ex:ssn`` will be validated against all three components.

---
---

The SHACL specification is divided into **SHACL Core** and **SHACL-SPARQL**.. **SHACL Core** consists of frequently needed features for the representation of shapes, constraints and targets. All SHACL implementations must at least implement SHACL Core. **SHACL-SPARQL** consists of all features of SHACL Core plus the advanced features of SPARQL-based constraints and an extension mechanism to declare new constraint components.

# Part 1: SHACL Core
## 2. Shapes and Constraints
The following informal diagram provides an overview of some of the key classes in the SHACL vocabulary. Each box represents a class. The content of the boxes under the class name lists some of the properties that instances of these classes may have, together with their value types. The arrows indicate `rdfs:subClassOf` triples.
![[Pasted image 20250530173623.png]]

---
### 2.1 Shapes
A shape is an **IRI** or **blank node** ``s`` that fulfills **at least one** of the following conditions in the **shapes graph**:
- `s` is a SHACL instance of `sh:NodeShape` or `sh:PropertyShape`.
- ``s`` is subject of a triple that has ``sh:targetClass``, ``sh:targetNode``, ``sh:targetObjectsOf`` or ``sh:targetSubjectsOf`` as **predicate**.
- ``s`` is **subject** of a triple that has a **parameter** as **predicate**.
- ``s`` is a value of a shape-expecting, non-list-taking parameter such as ``sh:node``, or a member of a SHACL list that is a value of a shape-expecting and list-taking parameter such as ``sh:or``.

**Informal explanation** of a Shape: A shape determines how to validate a focus node based on the values of properties and other characteristics of the focus node. For example, shapes can declare the condition that a focus node be an IRI or that a focus node has a particular value for a property and also a minimum number of values for the property.

The SHACL Core language defines two types of shapes:
- shapes about the focus node itself, called **node shapes**
- shapes about the values of a particular property or path for the focus node, called **property shapes**
`sh:Shape` is the SHACL superclass of those two shape types in the SHACL vocabulary. Its subclasses `sh:NodeShape` and `sh:PropertyShape` can be used as SHACL type of node and property shapes, respectively.

---
### 2.2 Node Shapes

Node shapes specify constraints that need to be met with respect to focus nodes. In contrast to property shapes, they primarily apply to the focus node itself, not to its property values.

---
### 2.3 Property Shapes

Property shapes specify constraints that need to be met with respect to nodes that can be reached from the focus node either by directly following a given property (specified as an IRI) or any other SHACL property path, specified using ``sh:path``.

---
---

## 3 Validation & Graphs

The input for a validation consists of a **data graph** and a **shapes graph**. After inputting those graphs and the validation process, you get a validation report which contains the results of the validation.
A validation system is called a **processor** and the verb **processing** is associated to the validation process.

An **RDF Validation Report Vocabulary** is used by the processors for producing validation reports as **RDF results graphs**.

---
### 3.3 Linking to shapes graphs (`sh:shapesGraph)

A **data graph** may include triples used to suggest one or more graphs to a SHACL processor with the predicate ``sh:shapesGraph``. Every value of ``sh:shapesGraph`` is an **IRI** representing a graph that should be included into the **shapes graph** used to validate the **data graph**.

---
### 3.4 Validation

**Validation** = mapping from input to validation results.

**Validation of a data graph against a shapes graph:** Given a **data graph** and a **shapes graph**, the validation results are the **union** of results of the validation of the data graph against **all** **shapes** in the shapes graph.

**Validation of a data graph against a shape:**  Given a **data graph** and a **shape** in the shapes graph, the validation results are the union of **the** results of the validation of all focus **nodes** that are in the **target of the shape** in the data graph.

**Validation of a focus node against a shape:** Given a **focus node** in the data graph and a **shape** in the shapes graph, the validation results are the **union** of the results of the validation of the **focus node** against **all constraints** declared by the **shape**, unless the shape has been deactivated, in which case the validation results are empty.

**Validation of a focus node against a constraint:** Given a **focus node** in the data graph and a **constraint of kind** ``C`` in the shapes graph, the validation results are defined by the **validators** of the **constraint component** ``C``. These validators typically take as **input** the **focus node**, the specific **values** of the **parameters of** ``C`` of the constraint in the shapes graph, and the **value nodes** of the shape that **declares the constraint**.

---
### 3.6 Validation Report

The **SHACL Validation Report Vocabulary** is used to describe the validation report. It defines the RDF properties in order to structural information which could lead to guidance on how identify / fix violations.

The result of a **validation process** consists of an RDF graph with one SHACL instance of `sh:ValidationReport`.
 
Example of a positive validation report:
```
[ 	a sh:ValidationReport ;
	sh:conforms true ; # no violations in data graph
] .
```

Example of a negative validation report:
```
[	a sh:ValidationReport ;
	sh:conforms false ;
	sh:result [
		a sh:ValidationResult ;
		sh:resultSeverity sh:Violation ;
		sh:focusNode ex:Bob ;
		sh:resultPath ex:age ;
		sh:value "twenty two" ;
		sh:resultMessage "ex:age expects a literal of datatype xsd:integer." ;
		sh:sourceConstraintComponent sh:DatatypeConstraintComponent ;
		sh:sourceShape ex:PersonShape-age ;
	]
] .
```

#### 3.6.1 Conforms (`sh:conforms`)

The value of this property is of datatype boolean. It shows the result of the conformance checking.

`sh: conforms` is true <=> validation didn't produce any validation results

#### 3.6.2 Result (`sh:result`)

For every validation result produced by a validation process, the SHACL instance of ``sh:ValidationReport`` has a value for the property `sh:result`. Each value of this type is a SHACL instance of the class ``sh:ValidationResult``.

=> every ``sh:result`` describes one validation failure.

#### 3.6.3 Syntax Checking of Shapes Graph (`sh:shapesGraphWellFormed`)

Indicates whether the shapes graph is well formed or not.

**Optional!**

#### 3.6.4 Validation Result (`sh:ValidationResult`)

one validation result <=> one failed validation

This is a subclass of s `sh:AbstractResult` to report individual SHACL validation results.

The properties `sh:focusNode`, `sh:resultSeverity` and `sh:sourceConstraintComponent`
are the only properties that are mandatory for all validation results.

#### 3.6.5 Focus Node (`sh:focusNode`)

This property indicates the focus node that has caused the failure / validation result. 

#### 3.6.6 Path (`sh:resultPath`)

Validation results may have a value for the property sh:resultPath pointing at a well-formed SHACL property path. For results produced by a property shape, this SHACL property path is equivalent to the value of sh:path of the shape, unless stated otherwise.

#ChatGPT : the affected property.

#### 3.6.7 Value (`sh:value`)

#ChatGPT : the value that caused the failure.

#### 3.6.8 Source (`sh:sourceShape`)

The shape that the given focus node was validated against.
#### 3.6.9 Constraint Component (`sh:sourceConstraintComponent`)

This value is the IRI of the constraint component that caused the result.
#### 3.6.10 Details  (`sh:detail`)

The property `sh:detail` may link a (parent) result with one or more SHACL instances of `sh:AbstractResult` that can provide further details about the cause of the (parent) result.

#### 3.6.11 Message  (`sh:resultMessage`)

To communicate additional textual details to humans.

#### 3.6.12 Severity  (`sh:resultSeverity`)

This value is an IRI. The value gives information about severity, it is equal to the value of `sh:severity` of the shape in the shapes graph.