##########################################################################################
#####################                                        			##################
#####################    TRABAJO ORDINARIA BIOINFORMÁTICA R             ##################
#####################                                       			##################
##########################################################################################


### 1.- Carga el archivo de entrada "archivo-entrada.txt" correspondiente. 
### Recuerda incluir los nombres de las columnas como el encabezado.
### Examina el archivo con las funciones head(), tail() y dim(). (1 pto)
datos <- read.delim("/Users/rutyy/Desktop/Bioinformática/carpeta R/Trabajo FINAL de R-20261014/archivo-entrada.txt", header= TRUE, check.names = FALSE) 
head(datos) 
tail(datos) 
dim(datos)

### 2.- En nuestra tabla tenemos los valores de 619 genes para tres réplicas
### del Control y tres réplicas de una Condición. Calcula la media y la desviación
### estándar del control y del tratamiento para cada gen. Puedes emplear cualquier
### función que consideres como apply(). Añade esos valores como columnas nuevas a tu tabla original. 
### Serán 4 columnas nuevas en total, la media de Control, la DE de Control, la media de Condición y la DE de Condición. (1,5 pto)

# Media y Desviación Estándar para el Control (columnas 2 a 4)
datos$media_control <- rowMeans(datos[, 2:4]) 
datos$DE_control <- apply(datos[, 2:4], 1, sd) 

#Media y Desviación Estándar para la Condición (columnas 5 a 7) 
datos$media_condicion <- rowMeans(datos[, 5:7]) 
datos$DE_condicion <- apply(datos[, 5:7], 1, sd) 
# Comprobamos cómo queda la tabla con las 4 columnas nuevas agregadas 
head(datos)

### 3.- En una sola imagen, muestra un histograma para la media del Control y otro para la media de la Condicíon.
### Pon colores diferentes en cada uno y mantén esos colores para el resto del trabajo. (1 pto).

#Cerramos cualquier dispositivo gráfico abierto para limpiar la pantalla - esto lo he tenido que buscar por que me salia una grafica en blanco y buscando se supone que es por que se quedaban ventanas abiertas.
while (dev.cur() > 1) dev.off() 

#Configuramos la ventana para 2 gráficos en una sola fila 
par(mfrow = c(1, 2)) 

#Dibujamos el histograma del Control 
hist(datos$media_control, col = "skyblue", main = "Control", xlab = "Media de expresión", ylab = "Número de genes") 

#Dibujamos el histograma de la Condición 
hist(datos$media_condicion, col = "salmon", main = "Condición", xlab = "Media de expresión", ylab = "Número de genes")


### 4.- En una sola imagen, muestra un boxplot para la condición y otro para el control. 
### Añade el título, colores y una una leyenda en la esquina superior izquierda. ( 1,5 pto)

#Guardamos la imagen en un archivo PNG
png("04_boxplot.png", width = 1000, height = 700) 
boxplot(datos$media_control, datos$media_condicion, names = c("Control", "Condición"), col = c("skyblue", "salmon"), main = "Expresión media de los genes", ylab = "Media de expresión") 
legend("topleft", legend = c("Control", "Condición"), fill = c("skyblue", "salmon"), bty = "n") 
dev.off() 

#Lo mostramos en la pantalla
boxplot(datos$media_control, datos$media_condicion, names = c("Control", "Condición"), col = c("skyblue", "salmon"), main = "Expresión media de los genes", ylab = "Media de expresión") 
legend("topleft", legend = c("Control", "Condición"), fill = c("skyblue", "salmon"), bty = "n")


### 5.- Evalúa la normalidad de Control y Condición y acorde con los resultados, haz lo siguiente: (2 pto)
### Realiza un test de comparativa de medias para cada gen entre condición y control. 
###	Guarda el p-value de la comparativa y anádelo como una columna extra a tu tabla original.

#Test de normalidad
shapiro.test(datos$media_control) 
shapiro.test(datos$media_condicion) 

#Creamos la columna vacía 
datos$p_value <- NA 

#Bucle para el t-test 
for (i in 1:nrow(datos)) { control <- as.numeric(datos[i, 2:4]); condicion <- as.numeric(datos[i, 5:7]); datos$p_value[i] <- t.test(control, condicion)$p.value } 

#Comprobamos que ya no salen NA sino valores numéricos de p-value 
head(datos)

### 6.- De los resultados del apartado 5, saca (mediante código) un listado de los genes diferencialmente expresados (aquellos que tengan un pvalue < 0.05)
### ¿Cuántos genes tienes? Sino te sale ninguno, justifica por qué. En caso de que sí que te salgan, ¿cuántos salen sobreexpresados y cuántos reprimidos? (1 pto)

#Filtramos los genes con p-value < 0.05 
genes_DE <- datos[datos$p_value < 0.05, ] 

#Mostramos los primeros genes del listado 
head(genes_DE[, c("Gene Name", "media_control", "media_condicion", "p_value")]) 

#Separamos entre sobreexpresados (media condición > media control)  y reprimidos (media condición < media control)
sobreexpresados <- genes_DE[genes_DE$media_condicion > genes_DE$media_control, ]; reprimidos <- genes_DE[genes_DE$media_condicion < genes_DE$media_control, ] 

#Resultados para responder a las preguntas del ejercicio: 
cat("Total de genes diferencialmente expresados (p < 0.05):", nrow(genes_DE), "\n") 
cat("Número de genes sobreexpresados:", nrow(sobreexpresados), "\n") 
cat("Número de genes reprimidos:", nrow(reprimidos), "\n")

### 7.- Por último, realiza un heatmap de los genes diferencialmente expresados
### Emplea la Práctica de R como referencia. (2 pts)

#Matriz de datos filtrados 
filtered <- as.matrix(genes_DE[, 2:7]) 
rownames(filtered) <- genes_DE$`Gene Name`

#Clústers de filas y columnas 
rowv <- as.dendrogram(hclust(as.dist(1 - cor(t(filtered))))) 
colv <- as.dendrogram(hclust(as.dist(1 - cor(filtered)))) 

#Heatmap básico en pantalla 
heatmap(filtered, Rowv = rowv, Colv = colv, cexCol = 0.7, labRow = FALSE) 

#Cargar paquetes 
if (!require("gplots")) install.packages("gplots") 
if(!require("RColorBrewer")) install.packages("RColorBrewer") 
library(gplots) 
library(RColorBrewer) 

# Heatmap avanzado en pantalla 
heatmap.2(filtered, Rowv = rowv, Colv = colv, cexCol = 0.7, col = rev(redblue(256)), scale = "row", labRow = FALSE) 

#Guardar en PDF 
pdf("GSE5583_DE_Heatmap.pdf") 
heatmap.2(filtered, Rowv = rowv, Colv = colv, cexCol = 0.7, col = rev(redblue(256)), scale = "row", labRow = FALSE) 
dev.off() 

#Guardar tabla de genes en fichero TXT 
write.table(filtered, "GSE5583_DE.txt", sep = "\t", quote = FALSE)

