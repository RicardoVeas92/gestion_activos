from django.db import models


# MANTENEDOR 1: Modelos de Impresora Base + Manual PDF (FileField)
class ModeloImpresora(models.Model):
    marca = models.CharField(max_length=50, default="HP", verbose_name="Marca")
    modelo = models.CharField(
        max_length=100, unique=True, verbose_name="Modelo"
    )
    tecnologia = models.CharField(
        max_length=50, default="Láser", verbose_name="Tecnología"
    )
    manual_pdf = models.FileField(
        upload_to="manuales/",
        blank=True,
        null=True,
        verbose_name="Manual / Ficha Técnica (PDF)",
    )

    def __str__(self):
        return f"{self.marca} {self.modelo}"

    class Meta:
        verbose_name = "Modelo de Impresora"
        verbose_name_plural = "Modelos de Impresoras"


# MANTENEDOR 1.B: Impresoras Instaladas en Clientes / Oficinas
class ImpresoraInstalada(models.Model):
    modelo = models.ForeignKey(
        ModeloImpresora,
        on_delete=models.CASCADE,
        related_name="instaladas",
        verbose_name="Modelo de Impresora",
    )
    numero_serie = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Número de Serie (S/N)",
    )
    oficina = models.CharField(max_length=150, verbose_name="Oficina / Área")
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ubicación Física / Dirección",
    )

    def __str__(self):
        return f"{self.modelo.modelo} - S/N: {self.numero_serie} ({self.oficina})"

    class Meta:
        verbose_name = "Impresora Instalada"
        verbose_name_plural = "Impresoras Instaladas"


# MANTENEDOR 2: Stock de Suministros y Repuestos + Fotografía (ImageField)
class ItemInventario(models.Model):
    TIPO_CHOICES = [
        ("SUMINISTRO", "Suministro (Tóner, Drum, etc.)"),
        ("REPUESTO", "Repuesto (Fusor, Rodillo, etc.)"),
    ]

    ESTADO_CHOICES = [
        ("DISPONIBLE", "Disponible en Stock La Serena"),
        ("INSTALADO", "Instalado / Utilizado"),
        ("DEFECTUOSO", "Defectuoso / Para Devolución"),
    ]

    numero_parte = models.CharField(
        max_length=100,
        verbose_name="Número de Parte (P/N)",
        help_text="Código del fabricante (ej: CF258A, W1410A)",
    )
    nombre = models.CharField(
        max_length=100, verbose_name="Descripción del Ítem"
    )
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Ítem"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="DISPONIBLE",
        verbose_name="Estado en Stock",
    )
    imagen = models.ImageField(
        upload_to="activos/",
        blank=True,
        null=True,
        verbose_name="Fotografía del Ítem",
    )

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.nombre} (P/N: {self.numero_parte}) - {self.get_estado_display()}"

    class Meta:
        verbose_name = "Ítem de Inventario"
        verbose_name_plural = "Inventario de Suministros y Repuestos"


# TRANSACCIÓN: Registro de Salida / Asignación de Suministro a Impresora Instalada
class RegistroUsoActivo(models.Model):
    ticket_santiago = models.CharField(
        max_length=50,
        verbose_name="N° Ticket Santiago",
        help_text="Número de ticket asignado desde Santiago.",
    )
    impresora_instalada = models.ForeignKey(
        ImpresoraInstalada,
        on_delete=models.CASCADE,
        related_name="usos",
        null=True,
        blank=True, 
        verbose_name="Impresora Atendida (S/N y Oficina)",
    )
    item_utilizado = models.ForeignKey(
        ItemInventario,
        on_delete=models.CASCADE,
        related_name="usos",
        verbose_name="Suministro / Repuesto Consumido",
    )
    fecha_uso = models.DateField(
        auto_now_add=True, verbose_name="Fecha de Instalación / Salida"
    )
    tecnico = models.CharField(
        max_length=100,
        default="Técnico La Serena",
        verbose_name="Técnico Ejecutor",
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Detalle del Trabajo / Observaciones",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item_utilizado.estado = "INSTALADO"
        self.item_utilizado.save()

    def __str__(self):
        return f"Ticket #{self.ticket_santiago} -> {self.impresora_instalada.oficina} ({self.item_utilizado.nombre})"

    class Meta:
        verbose_name = "Registro de Consumo / Salida"
        verbose_name_plural = "Registros de Consumo / Salidas"