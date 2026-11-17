# Guía de Interpretaciones Conceptuales - Teoría de la Información
## Unidades 4, 5 y 6 (Preparación para Parcial 2)

Esta guía reúne de manera sintética qué significa cada concepto, qué rescato al observar su valor numérico o resultado, cómo interpretarlo en un examen y con qué otros términos se relaciona.

---

# UNIDAD 4: Codificación de Fuente y Control de Errores

### 1. Entropía de la Fuente $H_r(S)$
* **¿Qué es?:** Medida promedio de la incertidumbre por símbolo antes de ser emitido, o la cantidad promedio de información que suministra la fuente al emitir un símbolo.
* **¿Qué miro en el valor?:**
  * Está acotada entre $0 \le H_r(S) \le \log_r(M)$ (donde $M$ es el tamaño del alfabeto fuente).
  * **$H = 0$:** Certeza absoluta (un solo símbolo tiene probabilidad 1). La fuente no aporta información.
  * **$H = \log_r(M)$:** Máxima incertidumbre (todos los símbolos son equiprobables).
  * **Límite teórico:** Representa la cota mínima física absoluta de bits/dígitos por símbolo necesarios para codificar la fuente sin pérdida.
* **Términos relacionados:** Información individual $I(s_i)$, Longitud media $L$, Primer Teorema de Shannon.

---

### 2. Longitud Media del Código ($L$ o $L_n$)
* **¿Qué es?:** Promedio ponderado de la cantidad de dígitos de código (bits si binario) utilizados para representar los símbolos de la fuente: $L = \sum P(s_i) \cdot l_i$.
* **¿Qué miro en el valor?:**
  * Siempre se compara con $H_r(S)$: se busca que $L$ sea lo más cercana posible a $H_r(S)$ sin ser inferior.
  * En una extensión de orden $N$, la longitud media por símbolo original es $L_n / N$.
* **Términos relacionados:** Entropía $H_r(S)$, Rendimiento $\eta$, Primer Teorema de Shannon.

---

### 3. Primer Teorema de Shannon (Teorema de Codificación de Fuente)
* **¿Qué expresa?:** Cota fundamental de compresión sin pérdida:
  $$H_r(S) \le \frac{L_n}{n} < H_r(S) + \frac{1}{n}$$
* **¿Cómo interpretarlo?:**
  * **Cota inferior ($L_n / n \ge H_r(S)$):** Ningún código decodificable unívocamente puede tener una longitud media menor a la entropía de la fuente. Si $L_n/n < H_r(S)$, el código es físicamente imposible o tiene pérdida.
  * **Cota superior ($L_n / n < H_r(S) + 1/n$):** Garantiza que siempre existe un código eficiente que cumple la cota.
  * **Efecto de la extensión ($n \to \infty$):** A medida que agrupamos símbolos en bloques más grandes ($n = 2, 3, \dots$), el término $1/n$ tiende a 0, haciendo que la longitud media por símbolo se acerque tanto como se desee a la entropía ($L_n/n \to H_r(S)$).
* **Términos relacionados:** Extensión de fuente $S^n$, Rendimiento $\eta$.

---

### 4. Rendimiento ($\eta$) y Redundancia ($R$)
* **Fórmulas:** $\eta = \frac{H_r(S)}{L}$, $\quad R = 1 - \eta$.
* **¿Qué miro en el valor?:**
  * **Rendimiento ($\eta$):** Mide la eficiencia del código (entre 0 y 1, o 0% a 100%). Representa la proporción de dígitos transmitidos que transportan información real.
    * $\eta = 1$ ($100\%$): Código óptimo/perfecto ($L = H_r$).
    * $\eta < 1$: Código ineficiente; hay dígitos redundantes.
  * **Redundancia ($R$):** Fracción de dígitos transmitidos que no aportan información nueva (sobrecarga).
    * En **compresión**, buscamos $R \to 0$.
    * En **control de errores**, la redundancia se añade intencionalmente para detectar y corregir fallos.
* **Términos relacionados:** Longitud media $L$, Entropía $H_r(S)$.

---

### 5. Distancia de Hamming ($d$ o $d_{\min}$)
* **¿Qué es?:** Cantidad mínima de posiciones en las que difieren dos palabras código válidas cualesquiera de un código de longitud fija.
* **¿Qué miro en el valor?:**
  * Mide la **separación geométrica** entre palabras válidas en el hipercubo binario.
  * A mayor distancia, más robusto es el código frente a alteraciones de bits por ruido.
* **Términos relacionados:** Errores detectables, Errores corregibles, Código de bloque.

---

### 6. Errores Detectables ($e_{\text{det}}$) y Errores Corregibles ($e_{\text{corr}}$)
* **Fórmulas:**
  $$e_{\text{det}} = d - 1, \qquad e_{\text{corr}} = \left\lfloor \frac{d - 1}{2} \right\rfloor$$
* **¿Cómo interpretarlo?:**
  * **Detectables ($d - 1$):** Si ocurren hasta $d - 1$ inversiones de bits, una palabra código válida se transforma en una cadena no válida (fuera del diccionario del código). El receptor sabe con certeza que hubo un error.
  * **Corregibles ($\lfloor(d - 1)/2\rfloor$):** Si ocurren hasta este número de errores, la palabra alterada sigue estando más cerca (en distancia de Hamming) de la palabra original enviada que de cualquier otra palabra válida (las esferas de radio $e_{\text{corr}}$ no se superponen). Por la regla de mínima distancia, se corrige automáticamente.
  * *Ejemplo:* Si $d = 4 \implies e_{\text{det}} = 3$ y $e_{\text{corr}} = 1$.

---

### 7. Paridad Vertical (VRC), Longitudinal (LRC) y Cruzada
* **Estructura:** Matriz de $(N+1) \times 8$. Fila 0 es VRC, columna 7 es LRC, esquina superior derecha (0, 7) es paridad cruzada.
* **¿Qué rescato al observar los fallos de paridad?:**
  * **0 filas con error y 0 columnas con error:** Mensaje perfecto, sin errores.
  * **Exactamente 1 fila ($i$) y 1 columna ($j$) con error:** Error simple (1 bit). Es **corregible**; el bit invertido está exactamente en la intersección $(i, j)$ y se invierte (`matriz[i][j] ^= 1`).
  * **Múltiples filas o columnas con error:** Error múltiple. Es **detectable pero no corregible**; se debe solicitar retransmisión.
  * Distancia del esquema: $d_{\min} = 4$ ($e_{\text{det}} = 3$, $e_{\text{corr}} = 1$).

---

# UNIDAD 5: Compresión de Datos

### 1. Código Compacto de Huffman vs Shannon-Fano
* **Huffman (Bottom-Up):**
  * Agrupa recursivamente los dos símbolos o ramas de menor probabilidad.
  * **Propiedad clave:** Garantiza un código de longitud mínima promedio (óptimo para codificación símbolo a símbolo).
* **Shannon-Fano (Top-Down):**
  * Ordena las probabilidades de mayor a menor y divide sucesivamente en dos subgrupos buscando que la suma de probabilidades de ambos sea lo más equitativa posible.
  * **Propiedad clave:** Es heurístico; suele dar códigos eficientes, pero en muchos casos genera una longitud media ligeramente superior a Huffman (subóptimo).
* **Comparación en examen:** Al comparar ambos códigos para la misma fuente:
  $$L_{\text{Huffman}} \le L_{\text{Shannon-Fano}} \implies \eta_{\text{Huffman}} \ge \eta_{\text{Shannon-Fano}}$$

---

### 2. Condición de Prefijo / Instantaneidad
* **¿Qué es?:** Ninguna palabra código es prefijo de otra.
* **¿Cómo interpretarlo?:** Permite que el receptor decodifique el mensaje símbolo a símbolo en tiempo real a medida que van llegando los bits, sin necesidad de esperar a recibir todo el bloque ni de insertar caracteres delimitadores (espacios o comas).

---

### 3. Tasa de Compresión ($N:1$)
* **Fórmula:** $\text{Tasa} = \frac{\text{Tamaño original}}{\text{Tamaño comprimido}}$.
* **¿Qué miro en el valor?:**
  * **$\text{Tasa} > 1$:** Hubo compresión efectiva (el archivo se redujo). Por ejemplo, tasa = 1.33 (o 4:3) significa que el original era 33% más grande que el comprimido.
  * **$\text{Tasa} = 1$:** No hubo ganancia de espacio.
  * **$\text{Tasa} < 1$:** Hubo **expansión de datos**. Ocurre cuando el overhead (bits de relleno o tuplas de compresión) supera al ahorro generado.

---

### 4. Run-Length Coding (RLC)
* **¿Qué es?:** Compresión por longitud de corridas. Codifica secuencias consecutivas repetidas del mismo carácter en pares `(carácter, cantidad)`.
* **¿Cuándo conviene?:**
  * Es altamente eficiente cuando el mensaje presenta rachas largas de caracteres idénticos (por ejemplo, `AAAAABBBBBB`).
  * Es contraproducente y genera expansión si el texto no tiene repeticiones consecutivas (por ejemplo, `ABCDE` pasa de 5 bytes a 10 bytes).

---

# UNIDAD 6: Canales de Información

### 1. Matriz del Canal $P(Y \mid X)$ y Probabilidades Condicionales
* **¿Qué representa?:** La ley física/probabilística del canal. Cada elemento $P(y_j \mid x_i)$ indica la probabilidad de que habiéndose emitido la entrada $x_i$, se reciba la salida $y_j$.
* **Propiedad obligatoria:** La suma de probabilidades de **cada fila siempre es igual a 1**.

---

### 2. Probabilidades a Posteriori $P(X \mid Y)$
* **¿Qué representan?:** La incertidumbre del receptor tras recibir el mensaje. Dado que en el destino se observó el símbolo $y_j$, ¿con qué probabilidad provino del símbolo de entrada $x_i$?
* **Fórmula (Bayes):** $P(x_i \mid y_j) = \frac{P(x_i) \cdot P(y_j \mid x_i)}{P(y_j)}$.
* **¿Qué miro en el valor?:**
  * Mide la **confiabilidad de la recepción**. Si una columna de $P(X \mid Y)$ tiene un valor cercano a 1, al recibir esa salida sabemos casi con total certeza qué entrada la causó.

---

### 3. Entropías a Posteriori $H(A \mid b_j)$
* **¿Qué es?:** La incertidumbre que le queda al observador sobre la entrada $A$ habiendo observado una salida particular $b_j$.
* **¿Qué miro en el valor?:**
  * **$H(A \mid b_j) = 0$:** Recepción ideal para ese símbolo. Al observar $b_j$, la incertidumbre sobre la entrada se desvanece por completo (hay un único $a_i$ con probabilidad 1).
  * **$H(A \mid b_j) > 0$:** Queda ambigüedad sobre qué entrada fue emitida al observar $b_j$.

---

### 4. Equivocación o Ruido $H(A/B)$
* **¿Qué es?:** El promedio ponderado de las entropías a posteriori: $H(A/B) = \sum_j P(b_j) H(A \mid b_j)$.
* **¿Cómo interpretarlo?:**
  * Mide la **incertidumbre media sobre la entrada que subsiste después de haber observado la salida**.
  * Representa la cantidad de información que el ruido "destruye" o borra en el canal.
  * **$H(A/B) = 0 \iff$ Canal Sin Ruido:** Toda la información emitida por la fuente puede ser deducida unívocamente a partir de la salida recibida.

---

### 5. Pérdida $H(B/A)$
* **¿Qué es?:** La incertidumbre media sobre qué salida se va a recibir conociendo de antemano qué entrada fue transmitida.
* **¿Cómo interpretarlo?:**
  * Mide la **dispersión o aleatoriedad que el canal introduce hacia adelante**.
  * **$H(B/A) = 0 \iff$ Canal Determinante:** Cada símbolo de entrada mapea a un único símbolo de salida con probabilidad 1 (no hay bifurcación de caminos).

---

### 6. Entropía Afín o Conjunta $H(A, B)$
* **¿Qué es?:** La incertidumbre global total del sistema entrada-salida considerado de manera simultánea.
* **Relaciones fundamentales:**
  $$H(A, B) = H(A) + H(B/A) = H(B) + H(A/B)$$
* **Límites:** $\max(H(A), H(B)) \le H(A, B) \le H(A) + H(B)$.

---

### 7. Información Mutua $I(A, B)$
* **¿Qué es?:** La cantidad neta de información que la salida aporta sobre la entrada (o viceversa). Es la información que **efectivamente atraviesa el canal con éxito**.
* **Relaciones de cálculo:**
  $$I(A, B) = H(A) - H(A/B)$$
  $$I(A, B) = H(B) - H(B/A)$$
  $$I(A, B) = H(A) + H(B) - H(A, B)$$
* **¿Qué rescato al observar su valor?:**
  * **$I(A, B) \ge 0$:** Siempre es mayor o igual a cero.
  * **Reciprocidad:** $I(A, B) = I(B, A)$ (la información mutua es simétrica).
  * **$I(A, B) = 0$:** La entrada y la salida son **estadísticamente independientes**. El canal es completamente inservible; observar la salida no reduce en absoluto la incertidumbre sobre la entrada.
  * **$I(A, B) = H(A)$:** Transmisión ideal sin pérdidas; toda la información de la fuente llega intacta.

---

### 8. Tipos Notables de Canales

| Tipo de Canal | Condición Matricial | Propiedad de Entropía | Información Mutua |
| :--- | :--- | :--- | :--- |
| **Sin Ruido** | Cada **columna** tiene a lo sumo un elemento $\ne 0$. | **Ruido:** $H(A/B) = 0$ | $I(A, B) = H(A)$ |
| **Determinante** | Cada **fila** tiene exactamente un elemento $\ne 0$ (vale 1). | **Pérdida:** $H(B/A) = 0$ | $I(A, B) = H(B)$ |
| **Sin Pérdida ni Ruido (Identidad / Permutación)** | Cada fila y cada columna tienen exactamente un 1. | $H(A/B) = 0$ y $H(B/A) = 0$ | $I(A, B) = H(A) = H(B)$ |
| **Uniforme** | Todas las filas son permutaciones de la primera fila. | $H(B/A) = H(\text{fila})$ (constante) | $I(A, B) = H(B) - H(\text{fila})$ |

---

### 9. Reducciones Suficientes de un Canal
* **¿Cuándo dos columnas $j$ y $k$ son combinables?:**
  * Cuando son **proporcionales fila por fila**: $\frac{P(y_j \mid x_i)}{P(y_k \mid x_i)} = \text{cte} \quad \forall i$.
* **¿Qué significa físicamente?:**
  * Recibir $y_j$ o recibir $y_k$ aporta exactamente la misma distribución de probabilidad a posteriori sobre la entrada ($P(X \mid y_j) = P(X \mid y_k)$).
  * Distinguir entre ambas salidas es un detalle superficial que no aporta información sobre la entrada.
* **Efecto de la reducción:**
  * Al fusionarlas mediante multiplicación por una matriz determinante, el canal se simplifica (se reduce el número de columnas) **sin perder nada de información mutua**:
    $$I(A, B_{\text{reducido}}) = I(A, B)$$

---

### 10. Canales en Serie (Teorema de Procesamiento de Datos)
* **Cálculo:** Matriz compuesta $M_{\text{comp}} = M_1 \times M_2$.
* **Interpretación:** Cada etapa adicional de transmisión o procesamiento nunca puede generar información nueva sobre la fuente original:
  $$I(A, C) \le \min\big(I(A, B), I(B, C)\big)$$
  * La equivocación total $H(A/C)$ siempre es mayor o igual a la de la primera etapa $H(A/B)$.

---

### 11. Capacidad del Canal ($C$)
* **¿Qué es?:** La máxima tasa teórica de transmisión de información confiable que el canal físico puede sostener:
  $$C = \max_{P(X)} I(A, B)$$
* **¿Cómo interpretarla?:**
  * Es una propiedad intrínseca del canal (de su matriz de transición), independiente de la fuente que conectemos.
  * **Casos especiales directos:**
    * **Canal Determinante:** $C = \log_2(\text{columnas alcanzables})$
    * **Canal Sin Ruido:** $C = \log_2(\text{número de entradas})$
    * **Canal Uniforme:** $C = \log_2(\text{columnas}) - H(\text{fila})$ (se alcanza cuando las entradas son equiprobables).
    * **Canal Binario General:** Se maximiza variando la probabilidad a priori $\omega \in [0, 1]$.

---

### 12. Probabilidad de Error del Canal ($P_E$)
* **¿Qué representa?:** La probabilidad promedio de que el receptor decida incorrectamente el símbolo de entrada tras recibir una salida particular.
* **Criterio de Máxima Posibilidad / Verosimilitud (ML - Convención de Cátedra):**
  * Para cada salida recibida $y$, se elige la entrada $x$ que maximiza el valor en la columna de la matriz del canal: $\max_x P(y \mid x)$.
  * **Acierto:** $P(\text{acierto}) = \sum_y P(x_{\text{elegido}}) \cdot P(y \mid x_{\text{elegido}})$.
  * **Error:** $P_E = 1 - P(\text{acierto})$.
* **¿Qué miro en el valor?:**
  * $P_E = 0 \implies$ Canal sin error bajo esa regla.
  * A menor $P_E$, mayor confiabilidad del canal bajo el criterio de decisión adoptado.

---

# Resumen de Fórmulas y Relaciones Clave para el Parcial

```text
                                  ┌─────────────────────────────┐
                                  │      H(A, B)  Afín          │
                                  └──────────────┬──────────────┘
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
    H(A) + H(B/A)  [Entrada + Pérdida]                          H(B) + H(A/B)  [Salida + Ruido]
                   │                                                           │
                   └─────────────────────────────┬─────────────────────────────┘
                                                 │
                                                 ▼
                           I(A, B) = H(A) - H(A/B) = H(B) - H(B/A)
```

* **Relaciones directas:**
  * $H(A/B) = H(A, B) - H(B)$
  * $H(B/A) = H(A, B) - H(A)$
  * $I(A, B) = H(A) + H(B) - H(A, B)$
  * Si el canal es **sin ruido** ($H(A/B) = 0$): $I(A, B) = H(A)$ y $H(A, B) = H(B)$.
  * Si el canal es **determinante** ($H(B/A) = 0$): $I(A, B) = H(B)$ y $H(A, B) = H(A)$.
  * Si el canal es **independiente** ($I(A, B) = 0$): $H(A, B) = H(A) + H(B)$, $H(A/B) = H(A)$, $H(B/A) = H(B)$.
