# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service/proto/component_snapshot.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&service/proto/component_snapshot.proto\x12\x1droblox.girp.componentSnapshot\"u\n\x11GetCamerasRequest\x12\x14\n\x0craw_metadata\x18\x01 \x01(\t\x12\x10\n\x08\x61sset_id\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x12\n\nasset_type\x18\x04 \x01(\t\x12\x13\n\x0bsnapshot_id\x18\x05 \x01(\t\"R\n\x08Metadata\x12\x46\n\x0fobject_metadata\x18\x01 \x03(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata\"\xc5\x02\n\x0eObjectMetadata\x12<\n\nchild_meta\x18\x01 \x03(\x0b\x32(.roblox.girp.componentSnapshot.ChildMeta\x12\x0f\n\x07lineage\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\tobj_class\x18\x04 \x01(\t\x12\r\n\x05order\x18\x05 \x01(\x05\x12\x39\n\x08position\x18\x06 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.Position\x12\x11\n\tcamera_id\x18\x07 \x01(\t\x12\x39\n\x08rotation\x18\x08 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.Rotation\x12\n\n\x02id\x18\t \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x12\n\nproperties\x18\x0b \x01(\t\"4\n\tChildMeta\x12\x13\n\x0b\x63hild_class\x18\x01 \x01(\t\x12\x12\n\nchild_name\x18\x02 \x01(\t\"\xdb\x05\n\x10MetadataWithType\x12I\n\x05model\x18\x01 \x03(\x0b\x32:.roblox.girp.componentSnapshot.MetadataWithType.ModelEntry\x12P\n\tmesh_part\x18\x02 \x03(\x0b\x32=.roblox.girp.componentSnapshot.MetadataWithType.MeshPartEntry\x12V\n\x0cspecial_mesh\x18\x03 \x03(\x0b\x32@.roblox.girp.componentSnapshot.MetadataWithType.SpecialMeshEntry\x12G\n\x04tool\x18\x04 \x03(\x0b\x32\x39.roblox.girp.componentSnapshot.MetadataWithType.ToolEntry\x12\r\n\x05\x63ount\x18\x05 \x01(\x05\x1a[\n\nModelEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x05value\x18\x02 \x01(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata:\x02\x38\x01\x1a^\n\rMeshPartEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x05value\x18\x02 \x01(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata:\x02\x38\x01\x1a\x61\n\x10SpecialMeshEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x05value\x18\x02 \x01(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata:\x02\x38\x01\x1aZ\n\tToolEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x05value\x18\x02 \x01(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata:\x02\x38\x01\"\xcb\x03\n\x08MetaTree\x12\x41\n\x05sound\x18\x01 \x03(\x0b\x32\x32.roblox.girp.componentSnapshot.MetaTree.SoundEntry\x12\x41\n\x05image\x18\x02 \x03(\x0b\x32\x32.roblox.girp.componentSnapshot.MetaTree.ImageEntry\x12?\n\x04text\x18\x03 \x03(\x0b\x32\x31.roblox.girp.componentSnapshot.MetaTree.TextEntry\x12\x41\n\x05video\x18\x04 \x03(\x0b\x32\x32.roblox.girp.componentSnapshot.MetaTree.VideoEntry\x1a,\n\nSoundEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a,\n\nImageEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tTextEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a,\n\nVideoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xfb\x01\n\nSingleInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tfull_path\x18\x02 \x01(\t\x12\x12\n\nclass_name\x18\x03 \x01(\t\x12\x39\n\x08position\x18\x04 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.Position\x12\x0f\n\x07mesh_id\x18\x05 \x01(\t\x12\x12\n\ntexture_id\x18\x06 \x01(\t\x12\x11\n\tmesh_type\x18\x07 \x01(\t\x12\x0c\n\x04text\x18\x08 \x01(\t\x12\x11\n\timage_url\x18\t \x01(\t\x12\x11\n\tvideo_url\x18\n \x01(\t\x12\x11\n\tsound_url\x18\x0b \x01(\t\"W\n\rAllDescendent\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\x12\x37\n\x04info\x18\x02 \x03(\x0b\x32).roblox.girp.componentSnapshot.SingleInfo\"\xf5\x04\n\tRccOutput\x12\x1d\n\x15place_version_hash_id\x18\x01 \x01(\t\x12K\n\x15output_all_descendent\x18\x02 \x01(\x0b\x32,.roblox.girp.componentSnapshot.AllDescendent\x12I\n\x10output_human_bfs\x18\x03 \x01(\x0b\x32/.roblox.girp.componentSnapshot.MetadataWithType\x12\x42\n\toutput_ml\x18\x04 \x01(\x0b\x32/.roblox.girp.componentSnapshot.MetadataWithType\x12:\n\tmeta_tree\x18\x05 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.MetaTree\x12\x46\n\x15meta_tree_dup_removed\x18\x06 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.MetaTree\x12\x45\n\x0e\x63\x61mera_results\x18\x07 \x03(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata\x12H\n\x08metadata\x18\x08 \x03(\x0b\x32\x36.roblox.girp.componentSnapshot.RccOutput.MetadataEntry\x1aX\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.roblox.girp.componentSnapshot.Metadata:\x02\x38\x01\"+\n\x08Position\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\x12\t\n\x01z\x18\x03 \x01(\x01\"\'\n\x04\x41xis\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\x12\t\n\x01z\x18\x03 \x01(\x01\"\x86\x01\n\x08Rotation\x12\x31\n\x04\x61xis\x18\x01 \x01(\x0b\x32#.roblox.girp.componentSnapshot.Axis\x12\r\n\x05\x61ngle\x18\x02 \x01(\x01\x12\x38\n\x0blook_vector\x18\x03 \x01(\x0b\x32#.roblox.girp.componentSnapshot.Axis\"\xae\x03\n\x17ProcessedObjectMetadata\x12\x13\n\x0bprimary_key\x18\x01 \x01(\t\x12\x19\n\x11place_snapshot_id\x18\x02 \x01(\x03\x12\x10\n\x08place_id\x18\x03 \x01(\x03\x12\x15\n\rplace_version\x18\x04 \x01(\x05\x12\x11\n\tobject_id\x18\x05 \x01(\t\x12?\n\x08metadata\x18\x06 \x01(\x0b\x32-.roblox.girp.componentSnapshot.ObjectMetadata\x12\x11\n\tfilenames\x18\x07 \x03(\t\x12\x0f\n\x07\x63\x64n_url\x18\x08 \x03(\t\x12k\n\x11moderation_result\x18\t \x03(\x0b\x32L.roblox.girp.componentSnapshot.ProcessedObjectMetadata.ModerationResultEntryB\x02\x18\x01\x12\x1c\n\x14serialized_ml_result\x18\n \x01(\t\x1a\x37\n\x15ModerationResultEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x32\x7f\n\x11\x43omponentSnapshot\x12j\n\nGetCameras\x12\x30.roblox.girp.componentSnapshot.GetCamerasRequest\x1a(.roblox.girp.componentSnapshot.RccOutput\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service.proto.component_snapshot_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _METADATAWITHTYPE_MODELENTRY._options = None
  _METADATAWITHTYPE_MODELENTRY._serialized_options = b'8\001'
  _METADATAWITHTYPE_MESHPARTENTRY._options = None
  _METADATAWITHTYPE_MESHPARTENTRY._serialized_options = b'8\001'
  _METADATAWITHTYPE_SPECIALMESHENTRY._options = None
  _METADATAWITHTYPE_SPECIALMESHENTRY._serialized_options = b'8\001'
  _METADATAWITHTYPE_TOOLENTRY._options = None
  _METADATAWITHTYPE_TOOLENTRY._serialized_options = b'8\001'
  _METATREE_SOUNDENTRY._options = None
  _METATREE_SOUNDENTRY._serialized_options = b'8\001'
  _METATREE_IMAGEENTRY._options = None
  _METATREE_IMAGEENTRY._serialized_options = b'8\001'
  _METATREE_TEXTENTRY._options = None
  _METATREE_TEXTENTRY._serialized_options = b'8\001'
  _METATREE_VIDEOENTRY._options = None
  _METATREE_VIDEOENTRY._serialized_options = b'8\001'
  _RCCOUTPUT_METADATAENTRY._options = None
  _RCCOUTPUT_METADATAENTRY._serialized_options = b'8\001'
  _PROCESSEDOBJECTMETADATA_MODERATIONRESULTENTRY._options = None
  _PROCESSEDOBJECTMETADATA_MODERATIONRESULTENTRY._serialized_options = b'8\001'
  _PROCESSEDOBJECTMETADATA.fields_by_name['moderation_result']._options = None
  _PROCESSEDOBJECTMETADATA.fields_by_name['moderation_result']._serialized_options = b'\030\001'
  _GETCAMERASREQUEST._serialized_start=73
  _GETCAMERASREQUEST._serialized_end=190
  _METADATA._serialized_start=192
  _METADATA._serialized_end=274
  _OBJECTMETADATA._serialized_start=277
  _OBJECTMETADATA._serialized_end=602
  _CHILDMETA._serialized_start=604
  _CHILDMETA._serialized_end=656
  _METADATAWITHTYPE._serialized_start=659
  _METADATAWITHTYPE._serialized_end=1390
  _METADATAWITHTYPE_MODELENTRY._serialized_start=1012
  _METADATAWITHTYPE_MODELENTRY._serialized_end=1103
  _METADATAWITHTYPE_MESHPARTENTRY._serialized_start=1105
  _METADATAWITHTYPE_MESHPARTENTRY._serialized_end=1199
  _METADATAWITHTYPE_SPECIALMESHENTRY._serialized_start=1201
  _METADATAWITHTYPE_SPECIALMESHENTRY._serialized_end=1298
  _METADATAWITHTYPE_TOOLENTRY._serialized_start=1300
  _METADATAWITHTYPE_TOOLENTRY._serialized_end=1390
  _METATREE._serialized_start=1393
  _METATREE._serialized_end=1852
  _METATREE_SOUNDENTRY._serialized_start=1671
  _METATREE_SOUNDENTRY._serialized_end=1715
  _METATREE_IMAGEENTRY._serialized_start=1717
  _METATREE_IMAGEENTRY._serialized_end=1761
  _METATREE_TEXTENTRY._serialized_start=1763
  _METATREE_TEXTENTRY._serialized_end=1806
  _METATREE_VIDEOENTRY._serialized_start=1808
  _METATREE_VIDEOENTRY._serialized_end=1852
  _SINGLEINFO._serialized_start=1855
  _SINGLEINFO._serialized_end=2106
  _ALLDESCENDENT._serialized_start=2108
  _ALLDESCENDENT._serialized_end=2195
  _RCCOUTPUT._serialized_start=2198
  _RCCOUTPUT._serialized_end=2827
  _RCCOUTPUT_METADATAENTRY._serialized_start=2739
  _RCCOUTPUT_METADATAENTRY._serialized_end=2827
  _POSITION._serialized_start=2829
  _POSITION._serialized_end=2872
  _AXIS._serialized_start=2874
  _AXIS._serialized_end=2913
  _ROTATION._serialized_start=2916
  _ROTATION._serialized_end=3050
  _PROCESSEDOBJECTMETADATA._serialized_start=3053
  _PROCESSEDOBJECTMETADATA._serialized_end=3483
  _PROCESSEDOBJECTMETADATA_MODERATIONRESULTENTRY._serialized_start=3428
  _PROCESSEDOBJECTMETADATA_MODERATIONRESULTENTRY._serialized_end=3483
  _COMPONENTSNAPSHOT._serialized_start=3485
  _COMPONENTSNAPSHOT._serialized_end=3612
# @@protoc_insertion_point(module_scope)
