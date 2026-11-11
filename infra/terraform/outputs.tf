output "client_vm" {
  description = "Informações da VM cliente"
  value = {
    name = proxmox_virtual_environment_vm.client.name
    vmid = proxmox_virtual_environment_vm.client.vm_id
    ip   = "10.10.30.20"
  }
}

output "server_vm" {
  description = "Informações da VM servidor"
  value = {
    name = proxmox_virtual_environment_vm.server.name
    vmid = proxmox_virtual_environment_vm.server.vm_id
    ip   = "10.10.30.10"
  }
}
