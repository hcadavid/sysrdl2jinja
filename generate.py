from jinja2 import Template

with open('sysrdl_adoc_table.template') as file_:
    template = Template(file_.read())

r1field1 = dict(name="FieldA",rights="RW",address="0x0001")
r1field2 = dict(name="FieldB",rights="RW",address="0x0002")
r1field3 = dict(name="FieldC",rights="R",address="0x0003")
r1field4 = dict(name="FieldEx",rights="R",address="0x0003")


registry1 = dict(name="The reg 1", fields=[r1field1, r1field2, r1field3])
registry2 = dict(name="The reg 1", fields=[r1field1, r1field2, r1field3, r1field4])

print(template.render(registers=[registry1, registry2]))
