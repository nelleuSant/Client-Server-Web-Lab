resource "proxmox_virtual_environment_download_file" "debian_cloud_image" {
  content_type = "iso"
  datastore_id = var.image_storage
  node_name    = var.node_name

  url       = "https://cloud.debian.org/images/cloud/trixie/latest/debian-13-generic-amd64.qcow2"
  file_name = "debian-13-generic-amd64.img"
}
