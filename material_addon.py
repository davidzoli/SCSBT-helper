bl_info = {
 "name": "Convert material",
 "author": "David Zoltan (davidzoli)",
 "version": (1, 0),
 "blender": (2, 6, 4),
 "location": "View3D > Object > Move4 Object",
 "description": "Moves the active Object",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
 "category": "Material"}


import bpy

class ConvertMaterial(bpy.types.Operator):
    bl_idname = "object.convert_material"
    bl_label = "Convert BT Material"

    def execute(self, context):
        floats = ["add_ambient", "reflection", "reflection2", "shadow_bias", "shininess", "tint_opacity"]
        colors = ["diffuse", "env_factor", "specular"]
        sets   = ["fresnel", "tint"]                                                                                # tint seems to be a color!

        for key in context.active_object.active_material["scs_mat_options"].keys():
            newval = ''
            _key = key
            str(key+" found")
            # variable is a float
            if (_key in floats):
                newval = float(context.active_object.active_material["scs_mat_options"][_key])
            # variable is a color

            if (_key in colors):
                newval2 = list(map(float, context.active_object.active_material["scs_mat_options"][key].strip(")").lstrip("(").split(', ')))
                newval2[0] = convertColor(newval2[0])
                newval2[1] = convertColor(newval2[1])
                newval2[2] = convertColor(newval2[2])
                newval = ''
                newval = list(map(float, newval2))

            # variable is a set of floats
            if (_key in sets):
                newval = list(map(float, context.active_object.active_material["scs_mat_options"][_key].strip(")").lstrip("(").split(', ')))
            # aux
            if (_key.find("aux") >= 0):
                _key = _key.replace("[","").replace("]","")
                newval2 = list(map(float, context.active_object.active_material["scs_mat_options"][key].strip(")").lstrip("(").split(', ')))
                auxiliary_prop = getattr(context.active_object.active_material.scs_props, "shader_attribute_" + _key, None)
                # clean old values possible left from previous shader
                while len(auxiliary_prop) > 0:
                    auxiliary_prop.remove(0)
                for listval in newval2:
                    item = auxiliary_prop.add()
                    item.value = listval
                    item.aux_type = _key
                    str("shader_attribute_" + _key+" set to: "+str(listval))
            # set the attributes
            if (newval!=''):
                str("shader_attribute_"+_key+" set to: "+str(newval))
                setattr(context.active_object.active_material.scs_props, "shader_attribute_"+_key, newval)
            str("---")
        return {'FINISHED'}

class UpdateMaterial(bpy.types.Operator):
    bl_idname = "object.update_material"
    bl_label = "Update BT Material"

    def execute(self, context):
        colors = ["shader_attribute_diffuse", "shader_attribute_env_factor", "shader_attribute_specular"]
        for key in bpy.context.object.active_material.scs_props.keys():
            if (key in colors):
                bpy.context.object.active_material.scs_props[key][0] = convertColor(bpy.context.object.active_material.scs_props[key][0])
                bpy.context.object.active_material.scs_props[key][1] = convertColor(bpy.context.object.active_material.scs_props[key][1])
                bpy.context.object.active_material.scs_props[key][2] = convertColor(bpy.context.object.active_material.scs_props[key][2])
        return {'FINISHED'}

def convertColor(x):
    if(x > 0.0031308):
        return pow(x,1.0/2.4)*1.055-0.055
    else:
        return x*12.92

def register():
    bpy.utils.register_class(ConvertMaterial)
    bpy.utils.register_class(UpdateMaterial)

def unregister():
    bpy.utils.unregister_class(ConvertMaterial)
    bpy.utils.unregister_class(UpdateMaterial)

if __name__ == "__main__":
    register()