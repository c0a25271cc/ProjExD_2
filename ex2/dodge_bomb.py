import time
import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rect:pg.Rect) -> tuple[bool, bool]:# 戻り値2つなので、bool, bool
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right: # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom: # 縦方向判定
        tate = False
    return yoko, tate


# 演習1
def gameover(screen: pg.Surface) -> None: # 演習1
    """
    こうかとんに爆弾が着弾し、画面をブラックアウト
    黒い画像と「Game Over」の文字列を5秒間表示
    """
    black_sfc = pg.Surface((WIDTH, HEIGHT)) # 画面全体覆うsurface作る
    black_sfc.fill((0, 0, 0)) # surface 黒く塗りつぶす
    black_sfc.set_alpha(200) # 透明度を設定

    fonto = pg.font.Font(None, 80) # フォントサイズ80
    txt = fonto.render("Game over", True, (255, 255, 255)) #白地で"Gameover"とかかれたsurfaceを生成
    black_sfc.blit(txt, [400, 300]) # 黒い背景にsurfaceを文字を画面にはりつけ

    kk_img = pg.image.load("fig/8.png") # 泣いてるこうかとん読み込む
    black_sfc.blit(kk_img, (350, 300)) # こうかとんを黒い背景にはりつけ
    black_sfc.blit(kk_img, (700, 300)) # こうかとん2体目

    screen.blit(black_sfc, (0, 0))
    pg.display.update() # 画面表示アップデート
    time.sleep(5)
    return


# 演習 2
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大、加速する
    """
    bb_imgs = [] # 爆弾surfaceを保存するリスト

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r)) # r倍のsurface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) # Surfaceの中心にr倍の赤い円を書く
        bb_img.set_colorkey((0, 0, 0)) # 爆弾の四隅を透過させる
        bb_imgs.append(bb_img)

        bb_accs = [a for a in range(1, 11)] # 加速度のリスト

        return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 空のsurface
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10) # 赤い爆弾を作成
    bb_img.set_colorkey((0, 0, 0)) # 爆弾の四隅の黒を透過させる

    bb_imgs, bb_accs = init_bb_imgs() # 演習2：爆弾の大きさ、加速度を渡して呼び出す
    
    bb_rct = bb_img.get_rect()
    bb_rct.width = bb_img.get_rect().width # 演習2：こうかとんの大きさが変わったら、width属性を更新
    bb_rct.height = bb_img.get_rect().height # 演習2：こうかとんの大きさが変わったら、width属性を更新
    bb_rct.centerx = random.randint(0, WIDTH) # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT) # 縦座標用の乱数
    vx, vy = +5, +5 # 練習2 横、縦方向の速度設定
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # 練習4：kkとbbのrctが重なっていたら
            gameover(screen) # 演習1：爆弾当たったらゲームオーバー関数呼び出し
            return


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] # 横方向移動量
                sum_mv[1] += tpl[1] # 縦方向移動量

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # どこかしらはみでてる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 先ほどの動きをキャンセル
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy) # 爆弾を移動
        yoko, tate = check_bound(bb_rct)
        if not yoko: # yoko == False
            vx *= -1 # vxの符号反転
        if not tate:
            vy *= -1 # vyの符号反転

        screen.blit(bb_img, bb_rct) # 練習2：爆弾を表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
