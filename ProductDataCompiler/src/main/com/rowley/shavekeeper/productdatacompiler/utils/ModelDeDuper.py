from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductConsolidator import ProductConsolidator
from src.main.com.rowley.shavekeeper.productdatacompiler.models.ProductModelByBrandMap import ProductModelByBrandMap
from src.main.com.rowley.shavekeeper.productdatacompiler.web.FileHelper import load_consolidator, save_consolidator, \
    save_reconciler, load_file, save_file

reconciled_json = load_file("Reconciler_Reconciled", "../compiled_files/")
reconciled = ProductModelByBrandMap.from_json(reconciled_json)

consolidated_json = load_file("ConsolidatedProducts1", "../compiled_files/")
base_consolidated = ProductConsolidator.from_json(consolidated_json)

deduped = ProductConsolidator()

total_pre = 0
total_post = 0

for brand in base_consolidated.pre_shaves:
    for model in base_consolidated.pre_shaves[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_pre_shave = base_consolidated.pre_shaves[brand][model]
            reconciled_pre_shave = reconciled.brands[brand][model]
            consolidated_pre_shave["brand"] = reconciled_pre_shave["brand"]
            consolidated_pre_shave["model"] = reconciled_pre_shave["model"]
            deduped.add_pre_shave(consolidated_pre_shave)

for brand in base_consolidated.soaps:
    for model in base_consolidated.soaps[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_soap = base_consolidated.soaps[brand][model]
            reconciled_soap = reconciled.brands[brand][model]
            consolidated_soap["brand"] = reconciled_soap["brand"]
            consolidated_soap["model"] = reconciled_soap["model"]
            deduped.add_soap(consolidated_soap)

for brand in base_consolidated.brushes:
    for model in base_consolidated.brushes[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_brush = base_consolidated.brushes[brand][model]
            reconciled_brush = reconciled.brands[brand][model]
            consolidated_brush["brand"] = reconciled_brush["brand"]
            consolidated_brush["model"] = reconciled_brush["model"]
            deduped.add_brush(consolidated_brush)

for brand in base_consolidated.razors:
    for model in base_consolidated.razors[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_razor = base_consolidated.razors[brand][model]
            reconciled_razor = reconciled.brands[brand][model]
            consolidated_razor["brand"] = reconciled_razor["brand"]
            consolidated_razor["model"] = reconciled_razor["model"]
            deduped.add_razor(consolidated_razor)

for brand in base_consolidated.blades:
    for model in base_consolidated.blades[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_blade = base_consolidated.blades[brand][model]
            reconciled_blade = reconciled.brands[brand][model]
            consolidated_blade["brand"] = reconciled_blade["brand"]
            consolidated_blade["model"] = reconciled_blade["model"]
            deduped.add_blade(consolidated_blade)

for brand in base_consolidated.post_shaves:
    for model in base_consolidated.post_shaves[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_post_shave = base_consolidated.post_shaves[brand][model]
            reconciled_post_shave = reconciled.brands[brand][model]
            consolidated_post_shave["brand"] = reconciled_post_shave["brand"]
            consolidated_post_shave["model"] = reconciled_post_shave["model"]
            deduped.add_post_shave(consolidated_post_shave)

for brand in base_consolidated.after_shaves:
    for model in base_consolidated.after_shaves[brand]:
        total_pre += 1
        if brand in reconciled.brands and model in reconciled.brands[brand]:
            # print "handling brand: " + brand + " model: " + model
            consolidated_after_shave = base_consolidated.after_shaves[brand][model]
            reconciled_after_shave = reconciled.brands[brand][model]
            consolidated_after_shave["brand"] = reconciled_after_shave["brand"]
            consolidated_after_shave["model"] = reconciled_after_shave["model"]
            deduped.add_after_shave(consolidated_after_shave)

for brand in deduped.pre_shaves:
    for model in deduped.pre_shaves[brand]:
        total_post += 1

for brand in deduped.soaps:
    for model in deduped.soaps[brand]:
        total_post += 1

for brand in deduped.brushes:
    for model in deduped.brushes[brand]:
        total_post += 1

for brand in deduped.razors:
    for model in deduped.razors[brand]:
        total_post += 1

for brand in deduped.blades:
    for model in deduped.blades[brand]:
        total_post += 1

for brand in deduped.post_shaves:
    for model in deduped.post_shaves[brand]:
        total_post += 1

for brand in deduped.after_shaves:
    for model in deduped.after_shaves[brand]:
        total_post += 1

print "Total Pre: " + str(total_pre)
print "Total Post: " + str(total_post)

save_file(deduped, "ConsolidatedProducts2", "../compiled_files/")