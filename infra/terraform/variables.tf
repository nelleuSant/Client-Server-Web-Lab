variable "proxmox_endpoint" {
  description = "URL da API do Proxmox, incluindo https:// e porta 8006"
  type        = string
}

variable "proxmox_api_token" {
  description = "Token no formato usuario@realm!tokenid=segredo"
  type        = string
  sensitive   = true
}

variable "proxmox_insecure" {
  description = "Ignora validação TLS; usar somente se necessário com certificado autoassinado"
  type        = bool
  default     = false
}

variable "node_name" {
  description = "Nome do nó Proxmox"
  type        = string
  default     = "pve"
}

variable "image_storage" {
  description = "Storage de diretório para armazenar a imagem cloud"
  type        = string
  default     = "local"
}

variable "vm_storage" {
  description = "Storage para discos das VMs e discos Cloud-Init"
  type        = string
  default     = "local-lvm"
}

variable "ssh_public_key_path" {
  description = "Caminho local da chave pública SSH"
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "ssh_private_key_path" {
  description = "Caminho local da chave privada SSH para conexão ao nó Proxmox"
  type        = string
  default     = "~/.ssh/id_ed25519"
}

variable "proxmox_ssh_address" {
  description = "Endereço IP ou hostname SSH do nó Proxmox"
  type        = string
  default     = "192.168.0.21"
}

variable "snippet_storage" {
  description = "Storage do Proxmox com suporte a snippets habilitado para arquivos Cloud-Init"
  type        = string
  default     = "local"
}

variable "temporary_internet_interface" {
  description = "Adiciona uma segunda interface vmbr0 temporária para instalação"
  type        = bool
  default     = false
}

variable "user_password_hash" {
  description = "Hash SHA-512 da senha do usuário Linux"
  type        = string
  sensitive   = true
}
