resource "proxmox_virtual_environment_vm" "server" {
  name      = "server01"
  vm_id     = 202
  node_name = var.node_name
  tags      = ["client-server", "server"]

  on_boot             = false
  stop_on_destroy     = true
  timeout_shutdown_vm = 60
  timeout_stop_vm     = 30

  agent {
    enabled = true
    timeout = "2m"
  }

  cpu {
    cores = 2
    type  = "host"
  }

  memory {
    dedicated = 3072
  }

  disk {
    datastore_id = var.vm_storage
    interface    = "scsi0"
    file_id      = proxmox_virtual_environment_download_file.debian_cloud_image.id
    size         = 30
    file_format  = "raw"
  }

  initialization {
    datastore_id      = var.vm_storage
    user_data_file_id = proxmox_virtual_environment_file.server_cloud_init.id

    # net0: rede privada, sem gateway.
    ip_config {
      ipv4 {
        address = "10.10.30.10/24"
      }
    }

    # net1: DHCP temporário pela vmbr0.
    dynamic "ip_config" {
      for_each = var.temporary_internet_interface ? [1] : []
      content {
        ipv4 {
          address = "dhcp"
        }
      }
    }
  }

  network_device {
    bridge  = "vmbr3"
    model   = "virtio"
    enabled = true
  }

  dynamic "network_device" {
    for_each = var.temporary_internet_interface ? [1] : []
    content {
      bridge  = "vmbr0"
      model   = "virtio"
      enabled = true
    }
  }

  operating_system {
    type = "l26"
  }

  serial_device {}
}
