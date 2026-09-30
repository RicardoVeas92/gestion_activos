from django.db import models


# MANTENEDOR 1: Modelos de Impresora + Manual de Servicio (FileField)
class ModeloImpresora(models.Model):
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    tecnologia = models.CharField(
        max_length=50, default="Láser Monocroma", verbose_name="Tecnología"
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


# MANTENEDOR 2: Inventario Local por Número de Parte + Fotografía (ImageField)
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
        help_text="Código o número de parte del fabricante (ej: CF258A, W1410A)",
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


# TRANSACCIÓN: Registro de Salida / Uso de Repuesto en Ticket de Santiago
class RegistroUsoActivo(models.Model):
    ticket_santiago = models.CharField(
        max_length=50,
        verbose_name="N° Ticket asignado por Santiago",
        help_text="Número de ticket generado en Santiago para el servicio técnico o suministro.",
    )
    impresora = models.ForeignKey(
        ModeloImpresora,
        on_delete=models.CASCADE,
        related_name="usos",
        verbose_name="Modelo de Impresora Atendida",
    )
    item_utilizado = models.ForeignKey(
        ItemInventario,
        on_delete=models.CASCADE,
        related_name="usos",
        verbose_name="Suministro / Repuesto Utilizado",
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
        # Cambiamos el estado del ítem a INSTALADO automáticamente al asociarlo al ticket
        self.item_utilizado.estado = "INSTALADO"
        self.item_utilizado.save()

    def __str__(self):
        return f"Ticket #{self.ticket_santiago} - {self.item_utilizado.nombre}"

    class Meta:
        verbose_name = "Registro de Consumo / Salida"
        verbose_name_plural = "Registros de Consumo / Salidas"