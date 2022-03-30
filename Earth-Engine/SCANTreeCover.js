var table = ee.FeatureCollection("users/cdw0063/SCAN2053"),
    table2 = ee.FeatureCollection("users/cdw0063/SCAN2055"),
    table3 = ee.FeatureCollection("users/cdw0063/SCAN2056"),
    table4 = ee.FeatureCollection("users/cdw0063/SCAN2057"),
    table5 = ee.FeatureCollection("users/cdw0063/SCAN2078"),
    table6 = ee.FeatureCollection("users/cdw0063/SCAN2113"),
    table7 = ee.FeatureCollection("users/cdw0063/SCAN2114"),
    table8 = ee.FeatureCollection("users/cdw0063/SCAN2115"),
    table9 = ee.FeatureCollection("users/cdw0063/SCAN2173"),
    table10 = ee.FeatureCollection("users/cdw0063/SCAN2174"),
    table11 = ee.FeatureCollection("users/cdw0063/SCAN2175"),
    table12 = ee.FeatureCollection("users/cdw0063/SCAN2176"),
    table13 = ee.FeatureCollection("users/cdw0063/SCAN2178"),
    table14 = ee.FeatureCollection("users/cdw0063/SCAN2179"),
    table15 = ee.FeatureCollection("users/cdw0063/SCAN2180"),
    table16 = ee.FeatureCollection("users/cdw0063/SCAN2181"),
    table17 = ee.FeatureCollection("users/cdw0063/SCAN2182"),
    table18 = ee.FeatureCollection("users/cdw0063/SCAN2177");
    

//SELECT TABLE ABOVE BY CHANGING THE TABLE BELOW
var TABLE = table2;

//CREATE TABLE ID VAR FOR LATER USE
var ID = ee.String(TABLE.get("system:id").getInfo().slice(-8,100));
print('Running Script for: ', ID);

var SCANSITE = TABLE.geometry();
Map.addLayer(SCANSITE, {}, 'SCAN', false);
Map.centerObject(SCANSITE, 12);

//NLCD land data
var all_nlcd_data = ee.ImageCollection('USGS/NLCD_RELEASES/2019_REL/NLCD');

//SINGLE IMAGE PATHS --------------------------------------------------------------
//2001 image
var nlcd2001 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2001')).first();
var clipnlcd2001 = nlcd2001.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2001, {}, 'NLCD2001', false);

//2004 image
var nlcd2004 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2004')).first();
var clipnlcd2004 = nlcd2004.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2004, {}, 'NLCD2004', false);

//2006 image
var nlcd2006 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2006')).first();
var clipnlcd2006 = nlcd2006.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2006, {}, 'NLCD2006', false);

//2008 image
var nlcd2008 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2008')).first();
var clipnlcd2008 = nlcd2008.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2008, {}, 'NLCD2008', false);

//2011 image
var nlcd2011 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2011')).first();
var clipnlcd2011 = nlcd2011.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2011, {}, 'NLCD2011', false);

//2013 image
var nlcd2013 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2013')).first();
var clipnlcd2013 = nlcd2013.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2013, {}, 'NLCD2013', false);

//2016 image
var nlcd2016 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2016')).first();
var clipnlcd2016 = nlcd2016.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2016, {}, 'NLCD2016', false);

//2019 image
var nlcd2019 = all_nlcd_data.filter(ee.Filter.eq('system:index', '2019')).first();
var clipnlcd2019 = nlcd2019.select('landcover').clip(SCANSITE);
Map.addLayer(clipnlcd2019, {}, 'NLCD2019', false);

//END IMAGE PATHS ------------------------------------------------------------------

//TREE CLASS MAP LAYERS ------------------------------------------------------------
//2001 tree class layers
var deciduous_forest = clipnlcd2001.eq(41);
var evergreen_forest = clipnlcd2001.eq(42);
var mixed_forest = clipnlcd2001.eq(43);

Map.addLayer(deciduous_forest, {}, 'DF-2001', false);
Map.addLayer(evergreen_forest, {}, 'EF-2001', false);
Map.addLayer(mixed_forest, {}, 'MF-2001', false);

//2004 tree class layers
var deciduous_forest2004 = clipnlcd2004.eq(41);
var evergreen_forest2004 = clipnlcd2004.eq(42);
var mixed_forest2004 = clipnlcd2004.eq(43);

Map.addLayer(deciduous_forest2004, {}, 'DF-2004', false);
Map.addLayer(evergreen_forest2004, {}, 'EF-2004', false);
Map.addLayer(mixed_forest2004, {}, 'MF-2004', false);

//2006 tree class layers
var deciduous_forest2006 = clipnlcd2006.eq(41);
var evergreen_forest2006 = clipnlcd2006.eq(42);
var mixed_forest2006 = clipnlcd2006.eq(43);

Map.addLayer(deciduous_forest2006, {}, 'DF-2006', false);
Map.addLayer(evergreen_forest2006, {}, 'EF-2006', false);
Map.addLayer(mixed_forest2006, {}, 'MF-2006', false);

//2008 tree class layers
var deciduous_forest2008 = clipnlcd2008.eq(41);
var evergreen_forest2008 = clipnlcd2008.eq(42);
var mixed_forest2008 = clipnlcd2008.eq(43);

Map.addLayer(deciduous_forest2008, {}, 'DF-2008', false);
Map.addLayer(evergreen_forest2008, {}, 'EF-2008', false);
Map.addLayer(mixed_forest2008, {}, 'MF-2008', false);

//2011 tree class layers
var deciduous_forest2011 = clipnlcd2011.eq(41);
var evergreen_forest2011 = clipnlcd2011.eq(42);
var mixed_forest2011 = clipnlcd2011.eq(43);

Map.addLayer(deciduous_forest2011, {}, 'DF-2011', false);
Map.addLayer(evergreen_forest2011, {}, 'EF-2011', false);
Map.addLayer(mixed_forest2011, {}, 'MF-2011', false);

//2013 tree class layers
var deciduous_forest2013 = clipnlcd2013.eq(41);
var evergreen_forest2013 = clipnlcd2013.eq(42);
var mixed_forest2013 = clipnlcd2013.eq(43);

Map.addLayer(deciduous_forest2013, {}, 'DF-2013', false);
Map.addLayer(evergreen_forest2013, {}, 'EF-2013', false);
Map.addLayer(mixed_forest2013, {}, 'MF-2013', false);

//2016 tree class layers
var deciduous_forest2016 = clipnlcd2016.eq(41);
var evergreen_forest2016 = clipnlcd2016.eq(42);
var mixed_forest2016 = clipnlcd2016.eq(43);

Map.addLayer(deciduous_forest2016, {}, 'DF-2016', false);
Map.addLayer(evergreen_forest2016, {}, 'EF-2016', false);
Map.addLayer(mixed_forest2016, {}, 'MF-2016', false);

//2019 tree class layers
var deciduous_forest2019 = clipnlcd2019.eq(41);
var evergreen_forest2019 = clipnlcd2019.eq(42);
var mixed_forest2019 = clipnlcd2019.eq(43);

Map.addLayer(deciduous_forest2019, {}, 'DF-2019', false);
Map.addLayer(evergreen_forest2019, {}, 'EF-2019', false);
Map.addLayer(mixed_forest2019, {}, 'MF-2019', false);
//END TREE CLASS MAP LAYERS --------------------------------------------------------

//ALL PIXEL CALCULATIONS -----------------------------------------------------------
//TOTAL AREA
var total_pixels = clipnlcd2001.gt(0).reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//ALL YEARS DF PIXELS 
//2001 
var total_df = deciduous_forest.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2004
var total_df2004 = deciduous_forest2004.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2006
var total_df2006 = deciduous_forest2006.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2008
var total_df2008 = deciduous_forest2008.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2011
var total_df2011 = deciduous_forest2011.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2013
var total_df2013 = deciduous_forest2013.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2016
var total_df2016 = deciduous_forest2016.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2019
var total_df2019 = deciduous_forest2019.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//END ALL DF PIXELS 

//ALL EF PIXELS 
//2001
var total_ef = evergreen_forest.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2004
var total_ef2004 = evergreen_forest2004.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//2006
var total_ef2006 = evergreen_forest2008.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2008
var total_ef2008 = evergreen_forest2008.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2011
var total_ef2011 = evergreen_forest2011.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//2013
var total_ef2013 = evergreen_forest2013.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//2016
var total_ef2016 = evergreen_forest2016.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//2019
var total_ef2019 = evergreen_forest2019.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});
//END ALL EF PIXELS 

//ALL MF PIXELS
//2001
var total_mf = mixed_forest.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2004
var total_mf2004 = mixed_forest2004.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2006
var total_mf2006 = mixed_forest2006.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2008
var total_mf2008 = mixed_forest2008.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2011
var total_mf2011 = mixed_forest2011.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2013
var total_mf2013 = mixed_forest2013.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2016
var total_mf2016 = mixed_forest2016.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//2019
var total_mf2019 = mixed_forest2019.reduceRegion({
  reducer: ee.Reducer.sum(), 
  geometry: SCANSITE,
  scale: 30,
  maxPixels: 1e9
});

//END ALL MF PIXELS 

//END ALL PIXEL CALCULATIONS -------------------------------------------------------------


//START PRINT STATEMENTS -----------------------------------------------------------------

//TREE PERCENT CALCULATIONS
//2001
var tree_percent = ee.Number(total_mf.get('landcover'))
.add(ee.Number(total_ef.get('landcover')))
.add(ee.Number(total_df.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2004
var tree_percent2004 = ee.Number(total_mf2004.get('landcover'))
.add(ee.Number(total_ef2004.get('landcover')))
.add(ee.Number(total_df2004.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2006
var tree_percent2006 = ee.Number(total_mf2006.get('landcover'))
.add(ee.Number(total_ef2006.get('landcover')))
.add(ee.Number(total_df2006.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2008
var tree_percent2008 = ee.Number(total_mf2008.get('landcover'))
.add(ee.Number(total_ef2008.get('landcover')))
.add(ee.Number(total_df2008.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2011
var tree_percent2011 = ee.Number(total_mf2011.get('landcover'))
.add(ee.Number(total_ef2011.get('landcover')))
.add(ee.Number(total_df2011.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2013
var tree_percent2013 = ee.Number(total_mf2013.get('landcover'))
.add(ee.Number(total_ef2013.get('landcover')))
.add(ee.Number(total_df2013.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2016
var tree_percent2016 = ee.Number(total_mf2016.get('landcover'))
.add(ee.Number(total_ef2016.get('landcover')))
.add(ee.Number(total_df2016.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);

//2019
var tree_percent2019 = ee.Number(total_mf2019.get('landcover'))
.add(ee.Number(total_ef2016.get('landcover')))
.add(ee.Number(total_df2016.get('landcover')))
.divide(ee.Number(total_pixels.get('landcover'))).multiply(100.0);
//END TREE PERCENT CALCULATIONS

//TOTAL TREES BY YEAR BY CLASS
//2001
var total_df2001 = ee.Number(total_df.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2001 = ee.Number(total_ef.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2001 = ee.Number(total_mf.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2004
var total_df2004 = ee.Number(total_df2004.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2004 = ee.Number(total_ef2004.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2004 = ee.Number(total_mf2004.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2006
var total_df2006 = ee.Number(total_df2006.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2006 = ee.Number(total_ef2006.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2006 = ee.Number(total_mf2006.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2008
var total_df2008 = ee.Number(total_df2008.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2008 = ee.Number(total_ef2008.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2008 = ee.Number(total_mf2008.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2011
var total_df2011 = ee.Number(total_df2011.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2011 = ee.Number(total_ef2011.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2011 = ee.Number(total_mf2011.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2013
var total_df2013 = ee.Number(total_df2013.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2013 = ee.Number(total_ef2013.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2013 = ee.Number(total_mf2013.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2016
var total_df2016 = ee.Number(total_df2016.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2016 = ee.Number(total_ef2016.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2016 = ee.Number(total_mf2016.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);

//2019
var total_df2019 = ee.Number(total_df2019.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_ef2019 = ee.Number(total_ef2019.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
var total_mf2019 = ee.Number(total_mf2019.get('landcover')).divide(total_pixels.get('landcover')).multiply(100);
//END TOTAL TREES BY YEAR BY CLASS

//TOTAL TREE COVER BY YEAR PRINT STATEMENTS
//2001
print('Total tree cover percent for all classes 2001:', tree_percent);

//2004
print('Total tree cover percent for all classes 2004:', tree_percent2004);

//2006
print('Total tree cover percent for all classes 2006:', tree_percent2006);

//2008
print('Total tree cover percent for all classes 2008:', tree_percent2008);

//2011
print('Total tree cover percent for all classes 2011:', tree_percent2011);

//2013
print('Total tree cover percent for all classes 2013:', tree_percent2013);

//2016
print('Total tree cover percent for all classes 2016:', tree_percent2016);

//2019
print('Total tree cover percent for all classes 2019:', tree_percent2019);

//END TOTAL TREE COVER BY YEAR PRINT STATEMENTS

//MEAN TREE COVER ALL YEARS
var mean_tree_cover_all_years = tree_percent.add(tree_percent2004).add(tree_percent2006)
.add(tree_percent2008).add(tree_percent2011).add(tree_percent2013).add(tree_percent2016)
.add(tree_percent2019).divide(8.0);

print('Mean tree cover 2001-2019:', mean_tree_cover_all_years);
//END MEAN TREE COVER ALL YEARS

//END ALL PRINT STATEMENTS ---------------------------------------------------------

//BEGIN FEATURE CONSTRUCTION -------------------------------------------------------

var tree_list = [
  //2001
  'Tree Cover 2001', ee.Number(tree_percent),
  'Total Deciduous 2001', ee.Number(total_df2001),
  'Total Evergreen 2001', ee.Number(total_ef2001),
  'Total Mixed 2001', ee.Number(total_mf2001),
  
  //2004
  'Tree Cover 2004', ee.Number(tree_percent2004),
  'Total Deciduous 2004', ee.Number(total_df2004),
  'Total Evergreen 2004', ee.Number(total_ef2004),
  'Total Mixed 2004', ee.Number(total_mf2004), 
  
  //2006
  'Tree Cover 2006', ee.Number(tree_percent2006),
  'Total Deciduous 2006', ee.Number(total_df2006),
  'Total Evergreen 2006', ee.Number(total_ef2006),
  'Total Mixed 2006', ee.Number(total_mf2006), 
  
  //2008
  'Tree Cover 2008', ee.Number(tree_percent2008),
  'Total Deciduous 2008', ee.Number(total_df2008),
  'Total Evergreen 2008', ee.Number(total_ef2008),
  'Total Mixed 2008', ee.Number(total_mf2008),
  
  //2011
  'Tree Cover 2011', ee.Number(tree_percent2011),
  'Total Deciduous 2011', ee.Number(total_df2011),
  'Total Evergreen 2011', ee.Number(total_ef2011),
  'Total Mixed 2011', ee.Number(total_mf2011), 
  
  //2013
  'Tree Cover 2013', ee.Number(tree_percent2013),
  'Total Deciduous 2013', ee.Number(total_df2013),
  'Total Evergreen 2013', ee.Number(total_ef2013),
  'Total Mixed 2013', ee.Number(total_mf2013),
  
  //2016
  'Tree Cover 2016', ee.Number(tree_percent2016),
  'Total Deciduous 2016', ee.Number(total_df2016),
  'Total Evergreen 2016', ee.Number(total_ef2016),
  'Total Mixed 2016', ee.Number(total_mf2016),
  
  //2019
  'Tree Cover 2019', ee.Number(tree_percent2019), 
  'Total Deciduous 2019', ee.Number(total_df2019),
  'Total Evergreen 2019', ee.Number(total_ef2019),
  'Total Mixed 2019', ee.Number(total_mf2019),
  
  //
  'Mean Tree Cover', ee.Number(mean_tree_cover_all_years)];

var dict = ee.Dictionary(tree_list);
print('Here is the final table :', dict)
Export.table.toDrive(ee.FeatureCollection(ee.Feature(null, dict)), 'Tree-Cover' + ID.getInfo(), 'SCANTreeCover', ID.getInfo(), 'CSV');