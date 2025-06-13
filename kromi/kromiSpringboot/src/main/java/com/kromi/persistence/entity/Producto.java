package com.kromi.persistence.entity;

import java.time.LocalDate;
import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "productos")
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer idProducto;

    @Column(name = "codigo_barras")
    private String codigoBarras;

    private String ean;

    @Column(name = "nombre_corto")
    private String nombreCorto;

    @Column(name = "nombre_completo")
    private String nombreCompleto;

    @Column(name = "descripcion_corta")
    private String descripcionCorta;

    @ManyToOne
    @JoinColumn(name = "categoria_id", insertable = false, updatable = false)
    private Integer categoriaId;

    private String produccion;

    @Column(name = "precio_lista")
    private Double precioLista;

    @Column(name = "revision_contenido")
    private  String revisionContenido;

    private String observaciones;
    private Boolean activo;

    private LocalDate fechaCreacion;
}
