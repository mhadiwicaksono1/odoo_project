{
    'name': 'Warehouse Contract',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Manage warehouse rental contracts and calculations',
    'description': """
        This module allows users to manage warehouse rental contracts,
        calculate billable months based on grace periods, and compute
        taxes and revenue sharing automatically.
    """,
    'author': 'Antigravity',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'reports/warehouse_contract_report.xml',
        'views/warehouse_contract_views.xml',
    ],
    'installable': True,
    'application': True,
}
