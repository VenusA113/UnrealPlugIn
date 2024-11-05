# Import various classes and functions from the Unreal module 
from unreal import (
    AssetToolsHelpers, # Tools for asset-related operations  
    EditorAssetLibrary, # Library for editor assets 
    AssetTools, # Asset tools interface 
    Material, # Material class 
    MaterialFactoryNew, # Factory class for creating new materials 
    MaterialEditingLibrary, # Library for editing materials 
    MaterialExpressionTextureSampleParameter2D as TexSample2D, # 2D texture sample expression 
    MaterialProperty, # Properties of materials 
    AssetImportTask, # Task for importing assets 
    FbxImportUI # User interface (UI) for FBX import options 

)
import os # Importing standard library modules/ Module for interacting with the operating system

class UnrealUtility: # Defining the UnrealUtility class 
    def __init__(self): # Initialization method for UnrealUtility class
        self.substanceRooDir='/game/Substance' # Root directory  for Substance files 
        self.substanceBaseMatName = 'M_SubstanceBase' # Name of the base material 
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName # Full path to the base material
        self.substanceTempfolder = '/game/Substance/temp' # Temporary folder for Substance files 
        self.baseColorName = "BaseColor" # Parameter name for the base color texture 
        self.normalName = "Normal" # Parameter name for the normal map texture 
        self.occRoughnessMatallic = "OcclusionRoughnessMetallic" # Parameter name for the occlusion, roughness, and metallic texture 

    def GetAssetTools()->AssetTools: # Method to get asset tools
       return AssetToolsHelpers.get_asset_tools() # Return the asset tools helper
    
    def ImportFromDir(self, dir): # Method to import assets from a directory 
        for file in os.listdir(dir): # Iterate over files in the specified directory 
            if "fbx" in file: # Checking if the file is an FBX file 
                self.LoadMeshFromPath(os.path.join(dir, file)) # Load the mesh from the file path 

    def LoadMeshFromPath(self, meshPath): # Method to load a mesh from a given path 
        print(f"loading fbx from {meshPath}") # Print the file path being loaded 
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "") # Get the mesh name by removing the .fbx extension 
        importTask = AssetImportTask() # Create a new asset import task 
        importTask.replace_existing = True # Set to replace existing assets 
        importTask.filename = meshPath # Set the file name for the import task 
        importTask.destination_path = '/game/' + meshName # Set the destination path in the game directory 
        importTask.save=True # Set to save the imported asset 

        fbxImportOption = FbxImportUI() # Create a new FBX import options object 
        fbxImportOption.import_mesh=True # Set to import the mesh 
        fbxImportOption.import_as_skeletal=False # Set to not import as a skeletal mesh 
        fbxImportOption.import_materials=False # Set to not import materials 
        fbxImportOption.static_mesh_import_data.combine_meshes=True # Set to combine meshes during import 
        importTask.option # Assign the import options to the import task

    def FindorBuildBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath): # Check if the base material already exists
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath) # Loadf and return the existing base material 
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew()) # Create a new base material 
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0) # Create a texture sample for the base color 
        baseColor.set_editor_property("parameter_name", self.baseColorName) # Set the parameter name for the base color texture 
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) # Connect the base color texture to the material's base color property 

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)  # Create a texture sample for the normal map
        normal.set_editor_property("parameter_name", self.normalName) # Set the parameter name for the normal map texture 
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) # Set the default normal texture
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)# Connect the normal map texture to the material's normal property 

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800) # Create a texture sample for the occlusion, roughness, and metallic map
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMatallic) # Set the parameter name for the occlusion, roughness, and metallic texture 
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) # Connect the "R" channel tot he material's ambient occlusion property
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS) # Connect the "G" channel to the material's roughness property 
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC) # Connect the "B" channel to the material's metallic property 

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) # Save the newly created base material 
        return baseMat # Return the base material 