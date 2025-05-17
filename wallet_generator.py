#!/usr/bin/env python3
"""
Generator Dompet Multi-Chain
Mendukung EVM, Sui, Solana, dan Aptos
"""

import sys
from typing import Dict, Tuple
from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44
from mnemonic import Mnemonic
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation

def tampilkan_pembukaan() -> None:
    """Menampilkan pesan pembuka"""
    print("\nGenerator Dompet Kripto")
    print("Mendukung jaringan EVM, Sui, Solana, dan Aptos")
    print("="*50)

class DompetSui:
    """Generator dompet Sui"""
    def __init__(self, mnemonic: str, password: str = '') -> None:
        self.mnemonic: str = mnemonic.strip()
        self.password: str = password
        self.pk_prefix: str = 'suiprivkey'
        self.ed25519_schema: str = '00'

    def dapatkan_alamat_dan_private_key(self, dengan_prefix=True) -> Tuple[str, str]:
        """Hasilkan alamat dan private key Sui"""
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate(self.password)
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SUI).DeriveDefaultPath()
        alamat = bip44_mst_ctx.PublicKey().ToAddress()
        private_key = bip44_mst_ctx.PrivateKey().Raw().ToHex()

        if dengan_prefix:
            pk_bytes_dengan_schema = bytes.fromhex(f'{self.ed25519_schema}{private_key}')
            private_key = f'{self.pk_prefix}{pk_bytes_dengan_schema.hex()}'

        return alamat, private_key

def buat_dompet_evm(mnemonic: str) -> Tuple[str, str]:
    """Hasilkan dompet EVM"""
    bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
    bip44_hdwallet.from_mnemonic(
        mnemonic=mnemonic,
        language="english",
        passphrase=None
    )
    bip44_hdwallet.clean_derivation()

    bip44_derivation = BIP44Derivation(
        cryptocurrency=EthereumMainnet,
        account=0,
        change=False,
        address=0
    )
    bip44_hdwallet.from_path(path=bip44_derivation)
    return bip44_hdwallet.address(), bip44_hdwallet.private_key()

def buat_dompet_solana(mnemonic: str) -> Tuple[str, str]:
    """Hasilkan dompet Solana"""
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA).DeriveDefaultPath()
    return bip44_mst_ctx.PublicKey().ToAddress(), bip44_mst_ctx.PrivateKey().Raw().ToHex()

def buat_dompet_aptos(mnemonic: str) -> Tuple[str, str]:
    """Hasilkan dompet Aptos"""
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.APTOS).DeriveDefaultPath()
    return bip44_mst_ctx.PublicKey().ToAddress(), bip44_mst_ctx.PrivateKey().Raw().ToHex()

def generate_dompet() -> None:
    """Fungsi utama pembuatan dompet"""
    tampilkan_pembukaan()
    
    try:
        jumlah = int(input("Berapa banyak dompet yang ingin dihasilkan? "))
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0")
        if jumlah > 100:
            print("Peringatan: Membuat lebih dari 100 dompet mungkin butuh waktu")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    hasil_wallet = []

    for i in range(jumlah):
        try:
            mnemonic = Mnemonic(language='english').generate(strength=128)
            
            # Buat semua jenis dompet
            alamat_evm, pk_evm = buat_dompet_evm(mnemonic)
            alamat_sui, pk_sui = DompetSui(mnemonic).dapatkan_alamat_dan_private_key()
            alamat_sol, pk_sol = buat_dompet_solana(mnemonic)
            alamat_apt, pk_apt = buat_dompet_aptos(mnemonic)

            # Format output
            wallet_info = f"""
Dompet #{i+1}
Mnemonic: {mnemonic}

[EVM]
Alamat: {alamat_evm}
Private Key: {pk_evm}

[Sui]
Alamat: {alamat_sui}
Private Key: {pk_sui}

[Solana]
Alamat: {alamat_sol}
Private Key: {pk_sol}

[Aptos]
Alamat: {alamat_apt}
Private Key: {pk_apt}
{'='*50}
"""
            hasil_wallet.append(wallet_info)
            print(wallet_info)

        except Exception as e:
            print(f"\nGagal membuat dompet {i+1}: {str(e)}")
            continue

    if hasil_wallet:
        try:
            with open('hasilwallet.txt', 'w', encoding='utf-8') as f:
                f.write("\n".join(hasil_wallet))
            print("\nData dompet berhasil disimpan ke 'hasilwallet.txt'")
        except Exception as e:
            print(f"\nGagal menyimpan ke file: {str(e)}")
    else:
        print("\nTidak ada dompet yang berhasil dibuat")

if __name__ == '__main__':
    try:
        generate_dompet()
    except KeyboardInterrupt:
        print("\nProses dibatalkan oleh pengguna")
        sys.exit(0)
    except Exception as e:
        print(f"\nError fatal: {str(e)}")
        sys.exit(1)
