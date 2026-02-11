from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.http import HttpResponse
from orders.models import Order
from accounts.models import Address
from datetime import datetime


def generate_invoice_pdf(order):
    """Generate PDF invoice for an order"""
    
    # Create HTTP response with PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    
    # Container for PDF elements
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_LEFT
    )
    
    # Header - Company Name
    story.append(Paragraph("🛍️ E-COMMERCE STORE", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Invoice Title and Details
    header_data = [
        ['INVOICE', f'Invoice #: ORD-{order.id}'],
        ['', f'Invoice Date: {datetime.now().strftime("%B %d, %Y")}'],
        ['', f'Order Date: {order.created_at.strftime("%B %d, %Y")}'],
    ]
    
    header_table = Table(header_data, colWidths=[2.5*inch, 3.5*inch])
    header_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 14),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#2c3e50')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Customer and Address Information
    address = Address.objects.filter(user=order.user).first()
    
    cust_data = [
        [
            [Paragraph("<b>BILL TO:</b>", heading_style),
             Paragraph(order.user.get_full_name() or order.user.username, normal_style),
             Paragraph(order.user.email, normal_style),
            ],
            [Paragraph("<b>SHIP TO:</b>", heading_style),
             Paragraph(address.full_name if address else order.user.get_full_name() or order.user.username, normal_style),
             Paragraph(address.address_line_1 if address else "No address available", normal_style),
             Paragraph(f"{address.city}, {address.state} {address.postal_code}" if address else "", normal_style),
             Paragraph(address.country if address else "", normal_style),
             Paragraph(f"Phone: {address.phone}" if address else "", normal_style),
            ]
        ]
    ]
    
    cust_table = Table(cust_data, colWidths=[3.25*inch, 3.25*inch])
    cust_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(cust_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Order Items Table
    items_data = [['Product', 'Qty', 'Price', 'Amount']]
    
    for item in order.items.all():
        items_data.append([
            item.product.name,
            str(item.quantity),
            f"₹{item.price:.2f}",
            f"₹{item.total_price:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Summary Table
    summary_data = [
        ['', 'Subtotal:', f'₹{order.total_price:.2f}'],
        ['', 'Tax (0%):', '₹0.00'],
        ['', 'Shipping:', 'FREE'],
        ['', 'TOTAL:', f'₹{order.total_price:.2f}'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (1, 3), (1, 3), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 3), (1, 3), 11),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Payment Status
    status_color = colors.HexColor('#27ae60') if order.is_paid else colors.HexColor('#e74c3c')
    status_text = "✓ PAID" if order.is_paid else "PENDING"
    
    status_style = ParagraphStyle(
        'Status',
        parent=styles['Normal'],
        fontSize=11,
        textColor=status_color,
        fontName='Helvetica-Bold'
    )
    
    story.append(Paragraph(f"Payment Status: {status_text}", status_style))
    
    if order.is_paid and order.paid_at:
        paid_date_style = ParagraphStyle(
            'PaidDate',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d')
        )
        story.append(Paragraph(f"Paid on: {order.paid_at.strftime('%B %d, %Y at %I:%M %p')}", paid_date_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("Thank you for your purchase! Please keep this invoice for your records.", footer_style))
    story.append(Paragraph("For support, visit: www.ecommerce.com | Email: support@ecommerce.com", footer_style))
    
    # Build PDF
    doc.build(story)
    
    return response
