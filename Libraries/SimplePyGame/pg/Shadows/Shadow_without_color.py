

class ShadowCaster:
    def init_shadow(self):
        self._shadow_surf = pg.Surface(self.hitbox.size, pg.SRCALPHA)

        self.draw_shadow_shape(self._shadow_surf, (255, 255, 255, 255))

    def cast_shadow(self):
        for light in App.Lights:
            direction = self.center - light.pos
            dist = direction.magnitude

            if dist > 0:
                shadow_len = max(self.shadow_info.minimal,
                                 min(dist * self.shadow_info.middle,
                                     self.shadow_info.maximal))

                offset = direction.normalized * shadow_len
                render_pos = self.pos + offset
                alpha_val = max(0, min(160, 180 - int(dist * 0.3)))


                self._shadow_surf.set_alpha(alpha_val)
                self._shadow_surf.fill((*light.color.rgb, alpha_val), special_flags=pg.BLEND_RGBA_MULT)

                self.screen.blit(self._shadow_surf, render_pos.xy)

