
import frappe
import xml.etree.ElementTree as ET

def import_xml(file_path):
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespaces
        namespaces = {
            k: v for k, v in [node for _, node in ET.iterparse(file_path, events=['start-ns'])]
        }

        # Extract general invoice details
        invoice_data = {
            "serie": root.attrib.get("Serie"),
            "folio": root.attrib.get("Folio"),
            "fecha": root.attrib.get("Fecha"),
            "subtotal": root.attrib.get("SubTotal"),
            "total": root.attrib.get("Total"),
            "moneda": root.attrib.get("Moneda"),
            "tipo_de_comprobante": root.attrib.get("TipoDeComprobante"),
            "metodo_pago": root.attrib.get("MetodoPago"),
            "lugar_expedicion": root.attrib.get("LugarExpedicion"),
        }

        # Create the Invoice DocType
        invoice = frappe.get_doc({
            "doctype": "Invoice",
            **invoice_data
        })
        invoice.insert()

        # Extract and create Concept DocTypes
        conceptos = root.find("cfdi:Conceptos", namespaces)
        if conceptos is not None:
            for concepto in conceptos.findall("cfdi:Concepto", namespaces):
                concept_data = {
                    "parent_invoice": invoice.name,
                    "descripcion": concepto.attrib.get("Descripcion"),
                    "cantidad": concepto.attrib.get("Cantidad"),
                    "valor_unitario": concepto.attrib.get("ValorUnitario"),
                    "importe": concepto.attrib.get("Importe"),
                }
                concept = frappe.get_doc({
                    "doctype": "Concept",
                    **concept_data
                })
                concept.insert()

        # Extract and create Tax DocTypes
        impuestos = root.find("cfdi:Impuestos", namespaces)
        if impuestos is not None:
            traslados = impuestos.find("cfdi:Traslados", namespaces)
            if traslados is not None:
                for traslado in traslados.findall("cfdi:Traslado", namespaces):
                    tax_data = {
                        "parent_invoice": invoice.name,
                        "impuesto": traslado.attrib.get("Impuesto"),
                        "tipo_factor": traslado.attrib.get("TipoFactor"),
                        "tasa_o_cuota": traslado.attrib.get("TasaOCuota"),
                        "importe": traslado.attrib.get("Importe"),
                    }
                    tax = frappe.get_doc({
                        "doctype": "Tax",
                        **tax_data
                    })
                    tax.insert()

        return f"Invoice {invoice.name} imported successfully."

    except Exception as e:
        return f"Error importing XML: {str(e)}"
