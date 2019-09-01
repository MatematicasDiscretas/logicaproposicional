### Lógica Proposicional

El siguiente es un algoritmo para determinar si una formula de lógica proposional esta bien formada o no.

* Ejemplos de Fórmulas bien Formadas para una Signature  ∑ = { p,q,r,s}. 

```
1. (p → q)
2. (¬p)
3. ¬((p → q) ∧(¬s))
4. ⟘
5. ⟙
6. r
```

* Son Fórmulas Mal Formadas 

```
1. ⟘(p → q)
2. (¬p⟙)
3. ¬((p → q) ∧(¬s)))
```