
provider "proxmox" {
  endpoint  = var.proxmox_endpoint
  api_token = var.proxmox_api_token
  insecure  = var.proxmox_insecure

  ssh {
    agent       = true
    username    = "root"
    private_key = file(pathexpand(var.ssh_private_key_path))

    node {
      name    = var.node_name
      address = var.proxmox_ssh_address
    }
  }
}