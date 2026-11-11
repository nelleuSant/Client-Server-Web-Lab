

resource "proxmox_virtual_environment_file" "client_cloud_init" {
  content_type = "snippets"
  datastore_id = var.snippet_storage
  node_name    = var.node_name

  source_raw {
    data = templatefile("${path.module}/cloud-init/client.yaml", {
      ssh_public_key     = trimspace(file(pathexpand(var.ssh_public_key_path)))
      user_password_hash = var.user_password_hash
    })

    file_name = "client-cloud-init.yaml"
  }
}

resource "proxmox_virtual_environment_file" "server_cloud_init" {
  content_type = "snippets"
  datastore_id = var.snippet_storage
  node_name    = var.node_name

  source_raw {
    data = templatefile("${path.module}/cloud-init/server.yaml", {
      ssh_public_key     = trimspace(file(pathexpand(var.ssh_public_key_path)))
      user_password_hash = var.user_password_hash
    })

    file_name = "server-cloud-init.yaml"
  }
}

